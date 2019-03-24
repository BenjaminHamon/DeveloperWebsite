import subprocess

import commands.lint


def get_command_list():
	return [
		commands.lint,
	]


def load_configuration(environment):
	configuration = {
		"project": "bhamon-website",
		"project_name": "My Website (www.benjaminhamon.com)",
		"project_version": { "identifier": "1.0" },
	}

	configuration["project_version"]["revision"] = subprocess.check_output([ environment["git_executable"], "rev-parse", "--short=10", "HEAD" ]).decode("utf-8").strip()
	configuration["project_version"]["branch"] = subprocess.check_output([ environment["git_executable"], "rev-parse", "--abbrev-ref", "HEAD" ]).decode("utf-8").strip()
	configuration["project_version"]["numeric"] = "{identifier}".format(**configuration["project_version"])
	configuration["project_version"]["full"] = "{identifier}+{revision}".format(**configuration["project_version"])

	configuration["author"] = "Benjamin Hamon"
	configuration["author_email"] = "hamon.benjamin@gmail.com"
	configuration["project_url"] = "https://github.com/BenjaminHamon/MyWebsite"

	configuration["packages"] = [ "bhamon_website" ]

	return configuration
