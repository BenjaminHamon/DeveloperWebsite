import datetime
import glob
import os
import subprocess

import development.commands.clean
import development.commands.develop
import development.commands.distribute
import development.commands.lint


def get_command_list():
	return [
		development.commands.clean,
		development.commands.develop,
		development.commands.distribute,
		development.commands.lint,
	]


def load_configuration(environment):
	configuration = {
		"project": "bhamon-website",
		"project_name": "My Website (www.benjaminhamon.com)",
		"project_version": { "identifier": "3.0" },
	}

	branch = subprocess.check_output([ environment["git_executable"], "rev-parse", "--abbrev-ref", "HEAD" ]).decode("utf-8").strip()
	revision = subprocess.check_output([ environment["git_executable"], "rev-parse", "--short=10", "HEAD" ]).decode("utf-8").strip()
	revision_date = int(subprocess.check_output([ environment["git_executable"], "show", "--no-patch", "--format=%ct", revision ]).decode("utf-8").strip())
	revision_date = datetime.datetime.utcfromtimestamp(revision_date).replace(microsecond = 0).isoformat() + "Z"

	configuration["project_version"]["branch"] = branch
	configuration["project_version"]["revision"] = revision
	configuration["project_version"]["date"] = revision_date
	configuration["project_version"]["numeric"] = "{identifier}".format(**configuration["project_version"])
	configuration["project_version"]["full"] = "{identifier}+{revision}".format(**configuration["project_version"])

	configuration["author"] = "Benjamin Hamon"
	configuration["author_email"] = "hamon.benjamin@gmail.com"
	configuration["project_url"] = "https://github.com/BenjaminHamon/MyWebsite"
	configuration["copyright"] = "Copyright © 2019 Benjamin Hamon"

	configuration["development_dependencies"] = [ "pylint", "wheel" ]

	configuration["components"] = [
		{ "name": "bhamon-website", "path": ".", "packages": [ "bhamon_website" ] },
	]

	return configuration


def get_setuptools_parameters(configuration):
	return {
		"version": configuration["project_version"]["full"],
		"author": configuration["author"],
		"author_email": configuration["author_email"],
		"url": configuration["project_url"],
	}


def list_package_data(package, pattern_collection):
	all_files = []
	for pattern in pattern_collection:
		all_files += glob.glob(package + "/" + pattern, recursive = True)
	return [ os.path.relpath(path, package) for path in all_files ]
