import logging

import flask
import werkzeug


logger = logging.getLogger("Website")


def configure(application):
	application.jinja_env.trim_blocks = True
	application.jinja_env.lstrip_blocks = True


def register_routes(application):
	application.add_url_rule("/", methods = [ "GET" ], view_func = home)
	application.add_url_rule("/education", methods = [ "GET" ], view_func = education)
	application.add_url_rule("/work_experience", methods = [ "GET" ], view_func = work_experience)
	application.add_url_rule("/skills", methods = [ "GET" ], view_func = skills)


def log_request():
	logger.info("%s %s from %s", flask.request.method, flask.request.base_url, flask.request.environ["REMOTE_ADDR"])


def handle_error(exception):
	logger.error("Failed to process request on %s", flask.request.path, exc_info = True)
	error_code = 500
	if isinstance(exception, werkzeug.exceptions.HTTPException):
		error_code = exception.code
	return flask.render_template("error.html", title = "Error", message = str(exception)), error_code


def home():
	return flask.render_template("home.html", title = "Home")


def education():
	return flask.render_template("education.html", title = "Education")


def work_experience():
	return flask.render_template("work_experience.html", title = "Work Experience")


def skills():
	return flask.render_template("skills.html", title = "Skills")
