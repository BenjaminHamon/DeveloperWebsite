import argparse
import logging
import os

import configuration
import environment


logger = logging.getLogger("Main")


def main():
	current_directory = os.getcwd()
	script_path = os.path.realpath(__file__)
	workspace_directory = os.path.dirname(os.path.dirname(script_path))

	os.chdir(workspace_directory)

	try:
		environment_instance = environment.load_environment()
		configuration_instance = configuration.load_configuration(environment_instance)

		arguments = parse_arguments(environment_instance, configuration_instance)
		environment.configure_logging(logging.getLevelName(arguments.verbosity.upper()))

		show_project_information(configuration_instance, arguments.simulate)
		arguments.func(environment_instance, configuration_instance, arguments)

	finally:
		os.chdir(current_directory)


def parse_arguments(environment_instance, configuration_instance):
	all_log_levels = [ "debug", "info", "warning", "error", "critical" ]

	main_parser = argparse.ArgumentParser()
	main_parser.add_argument("--verbosity", choices = all_log_levels, default = "info", metavar = "<level>", help = "set the logging level (%s)" % ", ".join(all_log_levels))
	main_parser.add_argument("--simulate", action = "store_true", help = "perform a test run, without writing changes")

	subparsers = main_parser.add_subparsers(title = "commands", metavar = "<command>")
	subparsers.required = True

	for command_module in configuration.get_command_list():
		command_parser = command_module.configure_argument_parser(environment_instance, configuration_instance, subparsers)
		command_parser.set_defaults(func = command_module.run)

	return main_parser.parse_args()


def show_project_information(configuration_instance, simulate):
	logger.info("%s %s", configuration_instance["project_name"], configuration_instance["project_version"]["full"])
	logger.info("Script executing in %s %s", os.getcwd(), "(simulation)" if simulate else '')
	print("")


if __name__ == "__main__":
	main()
