import logging
import os


logger = logging.getLogger("Main")


def setup(configuration, package, simulate):
	logger.info("Generating metadata for '%s'", package)

	metadata_file_path = os.path.join(package, "__metadata__.py")
	metadata_content = "__version__ = \"%s\"\n" % configuration["project_version"]["full"]

	if not simulate:
		with open(metadata_file_path, "w") as metadata_file:
			metadata_file.writelines(metadata_content)
