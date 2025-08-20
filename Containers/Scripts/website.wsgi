# cspell:words levelname

# WSGI entry point for the website

import json
import logging
import os
import sys

from benjaminhamon_standard_extensions.logging import logging_helpers

import benjaminhamon_developer_website
from benjaminhamon_developer_website import application_factory


def configure_logging() -> None:
    message_format = "[{levelname}][{name}] {message}"
    date_format = logging_helpers.date_format_iso
    log_stream_verbosity = "info"

    logging.root.setLevel(logging.DEBUG)

    logging.addLevelName(logging.DEBUG, "Debug")
    logging.addLevelName(logging.INFO, "Info")
    logging.addLevelName(logging.WARNING, "Warning")
    logging.addLevelName(logging.ERROR, "Error")
    logging.addLevelName(logging.CRITICAL, "Critical")

    logging_helpers.configure_log_stream(logging.root, sys.stdout, log_stream_verbosity, message_format, date_format)

    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("Request").setLevel(logging.WARNING)


configure_logging()

application_information = "Development version"
if benjaminhamon_developer_website.__product__ is not None:
    application_information = benjaminhamon_developer_website.__product__ + " " + benjaminhamon_developer_website.__version__

logger = logging.getLogger("Main")
logger.info("%s", application_information)
logger.info("Running as WSGI application")

home_directory = os.path.dirname(os.path.dirname(__file__))
configuration_file_path = os.path.join(home_directory, "website.json")
with open(configuration_file_path, "r") as configuration_file:
    configuration = json.load(configuration_file)

application = application_factory.create_application(
    flask_secret_key = configuration["flask_secret_key"],
    metrics_token = configuration["metrics_token"])
