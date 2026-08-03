# cspell:words werkzeug

import datetime
import functools
import logging
from typing import Callable, List, Optional

import flask
import jinja2
import werkzeug.exceptions
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

import benjaminhamon_developer_website
from benjaminhamon_developer_website.application import Application
from benjaminhamon_developer_website.main_controller import MainController


main_logger = logging.getLogger("Website")
request_logger = logging.getLogger("Request")


def create_application(flask_secret_key: str, metrics_token: str, open_to_work: bool, server: Optional[str] = None) -> Application:
    flask_application = create_flask_application(flask_secret_key)

    flask_application.config.update(
        METRICS_TOKEN = metrics_token,
        OPEN_TO_WORK = open_to_work,
    )

    prometheus_metrics = create_metrics(server)
    application = Application(flask_application)
    main_controller = MainController()

    register_handlers(flask_application, application)
    register_routes(flask_application, main_controller)
    prometheus_metrics.init_app(flask_application)

    return application


def create_flask_application(secret_key: str) -> flask.Flask:
    flask_application = flask.Flask("benjaminhamon_developer_website")

    flask_application.config.update(
        SECRET_KEY = secret_key,
        SESSION_COOKIE_HTTPONLY = True,
        SESSION_COOKIE_SAMESITE = "Lax",
        SESSION_COOKIE_SECURE = True,
        PERMANENT_SESSION_LIFETIME = datetime.timedelta(days = 7),
    )

    flask_application.config["METADATA"] = {
        "product": benjaminhamon_developer_website.__product__,
        "copyright": benjaminhamon_developer_website.__copyright__,
        "version": benjaminhamon_developer_website.__version__,
        "date": benjaminhamon_developer_website.__date__,
        "sources_url": "https://github.com/BenjaminHamon/DeveloperWebsite",
        "contact_email": "development@benjaminhamon.com",
    }

    flask_application.jinja_env.undefined = jinja2.StrictUndefined
    flask_application.jinja_env.trim_blocks = True
    flask_application.jinja_env.lstrip_blocks = True

    flask_application.context_processor(lambda: { "url_for": versioned_url_for })

    return flask_application


def create_metrics(server: Optional[str] = None) -> PrometheusMetrics:
    if server is None:
        return PrometheusMetrics(None, group_by = "endpoint", metrics_decorator = metrics_authorization)
    if server == "gunicorn":
        return GunicornInternalPrometheusMetrics(None, group_by = "endpoint", metrics_decorator = metrics_authorization)
    raise ValueError("Unsupported server: '%s'" % server)


def register_handlers(flask_application: flask.Flask, application: Application) -> None:
    flask_application.log_exception = lambda exc_info: None
    flask_application.before_request(application.log_request)
    flask_application.before_request(application.refresh_session)
    for exception in werkzeug.exceptions.default_exceptions.values():
        flask_application.register_error_handler(exception, application.handle_error)


def register_routes(application: flask.Flask, main_controller: MainController) -> None:
    add_url_rule(application, "/en", [ "GET" ], main_controller.redirect_for_locale_en)
    add_url_rule(application, "/fr", [ "GET" ], main_controller.redirect_for_locale_fr)

    add_url_rule(application, "/", [ "GET" ], main_controller.home)
    add_url_rule(application, "/contact", [ "GET" ],  main_controller.contact)
    add_url_rule(application, "/education", [ "GET" ],  main_controller.education)
    add_url_rule(application, "/projects", [ "GET" ],  main_controller.projects)
    add_url_rule(application, "/skills", [ "GET" ],  main_controller.skills)
    add_url_rule(application, "/work_experience", [ "GET" ],  main_controller.work_experience)


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
