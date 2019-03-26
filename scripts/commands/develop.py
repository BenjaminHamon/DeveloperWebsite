import logging
import subprocess

import scripts.commands.distribute


logger = logging.getLogger("Main")


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable=unused-argument
	return subparsers.add_parser("develop", help = "setup workspace for development")


def run(environment, configuration, arguments): # pylint: disable=unused-argument
	for package in configuration["packages"]:
		scripts.commands.distribute.setup(configuration, package, arguments.simulate)
	print("")
	install(environment["python3_executable"], arguments.simulate)
	print("")


def install(python_executable, simulate):
	logger.info("Installing development dependencies")

	install_command = [ python_executable, "-m", "pip", "install", "--upgrade", "pylint", "wheel" ]
	logger.info("+ %s", " ".join(install_command))
	if not simulate:
		subprocess.check_call(install_command)
		print("")

	logger.info("Installing development packages")

	install_command = [ python_executable, "-m", "pip", "install", "--upgrade", "--editable", "." ]
	logger.info("+ %s", " ".join(install_command))
	if not simulate:
		subprocess.check_call(install_command)
		print("")
