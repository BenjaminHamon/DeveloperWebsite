import logging
import subprocess

import commands.distribute


logger = logging.getLogger("Main")


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable=unused-argument
	return subparsers.add_parser("develop", help = "setup workspace for development")


def run(environment, configuration, arguments): # pylint: disable=unused-argument
	for package in configuration["packages"]:
		commands.distribute.setup(configuration, package, arguments.simulate)
	print("")
	install(environment["python3_executable"], arguments.simulate)
	print("")


def install(python_executable, simulate):
	logger.info("Installing packages for development")

	install_command = [ python_executable, "-m", "pip", "install", "--editable", "." ]
	logger.info("+ %s", " ".join(install_command))
	if not simulate:
		subprocess.check_call(install_command)
