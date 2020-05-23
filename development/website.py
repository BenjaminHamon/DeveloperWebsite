import argparse
import logging
import os
import sys

import flask

import bhamon_website.website

sys.path.insert(0, os.path.join(sys.path[0], ".."))

import development.environment # pylint: disable = wrong-import-position


logger = logging.getLogger("Main")


def main():
	environment_instance = development.environment.load_environment()
	arguments = parse_arguments()
	development.environment.configure_logging(environment_instance, arguments)

	logging.getLogger("werkzeug").setLevel(logging.WARNING)

	application = create_application()
	application.run(host = arguments.address, port = arguments.port, debug = True)


def parse_arguments():
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument("--address", required = True, help = "set the address for the server to listen to")
	argument_parser.add_argument("--port", required = True, type = int, help = "set the port for the server to listen to")
	return argument_parser.parse_args()


def create_application():
	application = flask.Flask("bhamon_website")
	bhamon_website.website.configure(application, "Benjamin Hamon")
	bhamon_website.website.register_handlers(application)
	bhamon_website.website.register_routes(application)
	return application


if __name__ == "__main__":
	main()
