import json
import logging
import os

import benjaminhamon_developer_website
from benjaminhamon_developer_website import application_factory


logger = logging.getLogger("Main")

logger.info("Instancing application for WSGI (version: %s)", benjaminhamon_developer_website.__version__)

configuration_file_path = os.environ["APPLICATION_CONFIGURATION"]
with open(configuration_file_path, mode = "r", encoding = "utf-8") as configuration_file:
    configuration = json.load(configuration_file)

application = application_factory.create_application(
    flask_secret_key = configuration["flask_secret_key"],
    metrics_token = configuration["metrics_token"],
    open_to_work = configuration["open_to_work"],
    server = configuration["server"])
