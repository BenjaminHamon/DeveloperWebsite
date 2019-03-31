import argparse
import logging

import flask
import werkzeug

import bhamon_website.website

import scripts.environment


logger = logging.getLogger("Main")


def main():
	scripts.environment.configure_logging(logging.INFO)
	arguments = parse_arguments()

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

	application.before_request(bhamon_website.website.log_request)
	for exception in werkzeug.exceptions.default_exceptions:
		application.register_error_handler(exception, bhamon_website.website.handle_error)

	bhamon_website.website.register_routes(application)

	return application


if __name__ == "__main__":
	main()
