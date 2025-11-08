# cspell:words werkzeug

import logging
from typing import Any, Callable, Optional

import flask
import flask.typing
import werkzeug.exceptions

from benjaminhamon_developer_website import web_helpers


main_logger = logging.getLogger("Application")
request_logger = logging.getLogger("Request")


class Application:


    def __init__(self, flask_application: flask.Flask) -> None:
        self._flask_application = flask_application


    def __call__(self, environ: dict, start_response: Callable) -> Any:
        return self._flask_application(environ, start_response)


    def run(self, address: Optional[str] = None, port: Optional[int] = None, debug: Optional[bool] = None) -> None:
        self._flask_application.run(host = address, port = port, debug = debug)


    def check_request(self) -> None:
        requested_locale = self._get_requested_locale()
        if requested_locale is not None and requested_locale not in self._flask_application.config["LOCALE_SUPPORTED"]:
            raise werkzeug.exceptions.NotFound


    def log_request(self) -> None:
        request_logger.info("(%s) %s %s", flask.request.environ["REMOTE_ADDR"], flask.request.method, flask.request.base_url)


    def handle_error(self, exception: Any) -> flask.typing.ResponseReturnValue:
        status_code = exception.code if isinstance(exception, werkzeug.exceptions.HTTPException) and exception.code is not None else 500
        status_message = web_helpers.get_http_error_message(status_code)

        request_logger.error("(%s) %s %s (StatusCode: %s)",
            flask.request.environ["REMOTE_ADDR"], flask.request.method, flask.request.base_url, status_code, exc_info = True)

        if flask.request.url_rule is not None and flask.request.url_rule.rule == "/metrics":
            return "", status_code, { "Content-Type": "text/plain" }

        requested_locale = self._get_requested_locale()
        if requested_locale is None or requested_locale not in self._flask_application.config["LOCALE_SUPPORTED"]:
            requested_locale = self._flask_application.config["LOCALE_DEFAULT"]

        return flask.render_template(requested_locale + "/" + "error.html", message = status_message, status_code = status_code), status_code


    def _get_requested_locale(self) -> Optional[str]:
        if flask.request.url_rule is not None and flask.request.view_args is not None:
            return flask.request.view_args.get("locale", None)
        return flask.request.path.split("/")[1]
