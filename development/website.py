import argparse
import logging

import flask

import bhamon_website.website

import development.environment


logger = logging.getLogger("Main")


def main():
	development.environment.configure_logging(logging.INFO)
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
	bhamon_website.website.register_handlers(application)
	bhamon_website.website.register_routes(application)
	return application


if __name__ == "__main__":
	main()
