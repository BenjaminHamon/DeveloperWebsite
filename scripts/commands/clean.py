import logging
import os
import shutil


logger = logging.getLogger("Main")


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable=unused-argument
	return subparsers.add_parser("clean", help = "clean the workspace")


def run(environment, configuration, arguments): # pylint: disable=unused-argument
	clean(configuration, arguments.simulate)


def clean(configuration, simulate):
	logger.info("Cleaning the workspace")
	print("")

	directories_to_clean = [
		{ "display_name": "Build", "path": "build" },
		{ "display_name": "Distribution", "path": "dist" },
	]

	for package in configuration["packages"]:
		directories_to_clean += [ { "display_name": "Python cache", "path": os.path.join(package, "__pycache__") } ]
		directories_to_clean += [ { "display_name": "Python egg", "path": package + ".egg-info" } ]

	for directory in directories_to_clean:
		if os.path.exists(directory["path"]):
			logger.info("Removing directory '%s' (Path: '%s')", directory["display_name"], directory["path"])
			if not simulate:
				shutil.rmtree(directory["path"])

	for package in configuration["packages"]:
		metadata_file = os.path.join(package, "__metadata__.py")
		if os.path.exists(metadata_file):
			logger.info("Removing generated file '%s'", metadata_file)
			if not simulate:
				os.remove(metadata_file)
