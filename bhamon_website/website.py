import json
import logging
import os

import flask
import werkzeug

import bhamon_website
import bhamon_website.render


logger = logging.getLogger("Website")


def configure(application):
	application.config["WEBSITE_COPYRIGHT"] = bhamon_website.__copyright__
	application.config["WEBSITE_VERSION"] = bhamon_website.__version__
	application.config["WEBSITE_DATE"] = bhamon_website.__date__

	application.jinja_env.trim_blocks = True
	application.jinja_env.lstrip_blocks = True
	application.jinja_env.filters["render_text"] = bhamon_website.render.render_text
	application.jinja_env.filters["render_date"] = bhamon_website.render.render_date

	application.context_processor(lambda: { "url_for": versioned_url_for })


def register_routes(application):
	application.add_url_rule("/", methods = [ "GET" ], view_func = home)
	application.add_url_rule("/education", methods = [ "GET" ], view_func = education)
	application.add_url_rule("/work_experience", methods = [ "GET" ], view_func = work_experience)
	application.add_url_rule("/skills", methods = [ "GET" ], view_func = skills)


def log_request():
	logger.info("%s %s from %s", flask.request.method, flask.request.base_url, flask.request.environ["REMOTE_ADDR"])


def handle_error(exception):
	logger.error("Failed to process request on %s", flask.request.path, exc_info = True)
	status_code = exception.code if isinstance(exception, werkzeug.exceptions.HTTPException) else 500
	status_message = _get_error_message(status_code)
	return flask.render_template("error.html", title = "Error", message = status_message, status_code = status_code), status_code


def versioned_url_for(endpoint, **values):
	if endpoint == "static":
		values["version"] = flask.current_app.config["WEBSITE_VERSION"]
	return flask.url_for(endpoint, **values)


def home():
	view_data = {
		"identity": _load_content("static/identity/identity.json"),
		"contact": _load_content("static/contact/contact.json"),
		"introduction": _load_content("static/introduction/introduction.json"),
	}

	return flask.render_template("home.html", title = "Home", **view_data)


def education():
	view_data = {
		"education": _load_content("static/education/education.json"),
	}

	return flask.render_template("education.html", title = "Education", **view_data, encoding = "utf-8")


def work_experience():
	view_data = {
		"work_experience": _load_content("static/work_experience/work_experience.json"),
	}

	return flask.render_template("work_experience.html", title = "Work Experience", **view_data)


def skills():
	view_data = {
		"skill": _load_content("static/skill/skill.json"),
	}

	return flask.render_template("skills.html", title = "Skills", **view_data)


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
	with open(os.path.join(flask.current_app.root_path, file_path), encoding = "utf-8") as content_file:
		return json.load(content_file)
