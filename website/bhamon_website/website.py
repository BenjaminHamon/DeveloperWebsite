import json
import logging
import os

import flask
import jinja2
import werkzeug
import yaml

import bhamon_website
import bhamon_website.render


main_logger = logging.getLogger("Website")
request_logger = logging.getLogger("Request")


def configure(application, title):
	application.config["WEBSITE_TITLE"] = title
	application.config["WEBSITE_COPYRIGHT"] = bhamon_website.__copyright__
	application.config["WEBSITE_VERSION"] = bhamon_website.__version__
	application.config["WEBSITE_DATE"] = bhamon_website.__date__

	application.jinja_env.undefined = jinja2.StrictUndefined()
	application.jinja_env.trim_blocks = True
	application.jinja_env.lstrip_blocks = True
	application.jinja_env.filters["render_text"] = bhamon_website.render.render_text
	application.jinja_env.filters["render_date"] = bhamon_website.render.render_date

	application.context_processor(lambda: { "url_for": versioned_url_for })


def register_handlers(application):
	application.log_exception = lambda exc_info: None
	application.before_request(log_request)
	for exception in werkzeug.exceptions.default_exceptions:
		application.register_error_handler(exception, handle_error)


def register_routes(application):
	application.add_url_rule("/", methods = [ "GET" ], view_func = home)
	application.add_url_rule("/education", methods = [ "GET" ], view_func = education)
	application.add_url_rule("/skills", methods = [ "GET" ], view_func = skills)
	application.add_url_rule("/work_experience", methods = [ "GET" ], view_func = work_experience)


def log_request():
	request_logger.info("(%s) %s %s", flask.request.environ["REMOTE_ADDR"], flask.request.method, flask.request.base_url)


def handle_error(exception):
	status_code = exception.code if isinstance(exception, werkzeug.exceptions.HTTPException) else 500
	status_message = _get_error_message(status_code)
	request_logger.error("(%s) %s %s (StatusCode: %s)", flask.request.environ["REMOTE_ADDR"], flask.request.method, flask.request.base_url, status_code, exc_info = True)
	return flask.render_template("error.html", title = "Error", message = status_message, status_code = status_code), status_code


def versioned_url_for(endpoint, **values):
	if endpoint == "static":
		values["version"] = flask.current_app.config["WEBSITE_VERSION"]
	return flask.url_for(endpoint, **values)


def home():
	view_data = {
		"identity": _load_content("static/identity/identity.yaml"),
		"contact": _load_content("static/contact/contact.yaml"),
		"introduction": _load_content("static/introduction/introduction.yaml"),
	}

	return flask.render_template("home.html", title = "Home", **view_data)


def education():
	view_data = {
		"education": _load_content("static/education/education.yaml"),
	}

	return flask.render_template("education.html", title = "Education", **view_data, encoding = "utf-8")


def skills():
	view_data = {
		"skill": _load_content("static/skill/skill.yaml"),
	}

	return flask.render_template("skills.html", title = "Skills", **view_data)


def work_experience():
	view_data = {
		"work_experience": _load_content("static/work_experience/work_experience.yaml"),
	}

	return flask.render_template("work_experience.html", title = "Work Experience", **view_data)


def _get_error_message(status_code): # pylint: disable = too-many-return-statements
	if status_code == 400:
		return "Bad request"
	if status_code == 401:
		return "Unauthorized"
	if status_code == 403:
		return "Forbidden"
	if status_code == 404:
		return "Page not found"
	if status_code == 405:
		return "Method not allowed"

	if status_code == 500:
		return "Internal server error"

	if 400 <= status_code < 500:
		return "Client error"
	if 500 <= status_code < 600:
		return "Server error"
	return "Unknown error"


def _load_content(file_path):
	file_path = os.path.join(flask.current_app.root_path, file_path)
	with open(file_path, mode = "r", encoding = "utf-8") as content_file:
		if file_path.endswith(".json"):
			return json.load(content_file)
		if file_path.endswith(".yaml"):
			return yaml.safe_load(content_file)
		return content_file.read()
