# cspell:words werkzeug

import datetime
import functools
import logging
from typing import Callable, List

import flask
import jinja2
import prometheus_flask_exporter
import werkzeug.exceptions

import benjaminhamon_developer_website
from benjaminhamon_developer_website.application import Application
from benjaminhamon_developer_website.main_controller import MainController


main_logger = logging.getLogger("Website")
request_logger = logging.getLogger("Request")


def create_application(flask_secret_key: str, metrics_token: str) -> Application:
    flask_application = flask.Flask("benjaminhamon_developer_website")
    flask_application.secret_key = flask_secret_key
    flask_application.config.update(
        SECRET_KEY = flask_secret_key,
        SESSION_COOKIE_HTTPONLY = True,
        SESSION_COOKIE_SAMESITE = "Lax",
        SESSION_COOKIE_SECURE = True,
        PERMANENT_SESSION_LIFETIME = datetime.timedelta(days = 7),
        METRICS_TOKEN = metrics_token,
    )

    prometheus_metrics = prometheus_flask_exporter.PrometheusMetrics(None, metrics_decorator = metrics_authorization)
    application = Application(flask_application)
    main_controller = MainController()

    configure(flask_application)
    register_handlers(flask_application, application)
    register_routes(flask_application, main_controller)
    prometheus_metrics.init_app(flask_application)

    return application


def configure(application: flask.Flask) -> None:
    application.config["METADATA"] = {
        "product": benjaminhamon_developer_website.__product__,
        "copyright": benjaminhamon_developer_website.__copyright__,
        "version": benjaminhamon_developer_website.__version__,
        "date": benjaminhamon_developer_website.__date__,
        "sources_url": "https://github.com/BenjaminHamon/DeveloperWebsite",
        "contact_email": "development@benjaminhamon.com",
    }

    application.config["LOCALE_DEFAULT"] = "en"
    application.config["LOCALE_SUPPORTED"] = [ "en", "fr" ]

    application.jinja_env.undefined = jinja2.StrictUndefined
    application.jinja_env.trim_blocks = True
    application.jinja_env.lstrip_blocks = True

    application.context_processor(lambda: { "url_for": versioned_url_for })


def register_handlers(flask_application: flask.Flask, application: Application) -> None:
    flask_application.log_exception = lambda exc_info: None
    flask_application.before_request(application.log_request)
    flask_application.before_request(application.check_request)
    for exception in werkzeug.exceptions.default_exceptions.values():
        flask_application.register_error_handler(exception, application.handle_error)


def register_routes(application: flask.Flask, main_controller: MainController) -> None:
    add_url_rule(application, "/", [ "GET" ], main_controller.home_default)
    add_url_rule(application, "/<locale>", [ "GET" ], main_controller.home)
    add_url_rule(application, "/<locale>/contact", [ "GET" ],  main_controller.contact)
    add_url_rule(application, "/<locale>/education", [ "GET" ],  main_controller.education)
    add_url_rule(application, "/<locale>/projects", [ "GET" ],  main_controller.projects)
    add_url_rule(application, "/<locale>/skills", [ "GET" ],  main_controller.skills)
    add_url_rule(application, "/<locale>/work_experience", [ "GET" ],  main_controller.work_experience)


def add_url_rule(application: flask.Flask, path: str, methods: List[str], handler: Callable, **kwargs) -> None:
    endpoint = ".".join(handler.__module__.split(".")[1:]) + "." + handler.__name__
    application.add_url_rule(path, methods = methods, endpoint = endpoint, view_func = handler, **kwargs)


def versioned_url_for(endpoint: str, **values) -> str:
    if endpoint == "static":
        values["version"] = flask.current_app.config["METADATA"]["version"]
    return flask.url_for(endpoint, **values)


def metrics_authorization(view_function):
    @functools.wraps(view_function)

    def decorated_function(*args, **kwargs):
        if flask.request.authorization is None:
            flask.abort(401)

        token = flask.request.authorization.token
        if token != flask.current_app.config["METRICS_TOKEN"]:
            flask.abort(403)

        return view_function(*args, **kwargs)

    return decorated_function
