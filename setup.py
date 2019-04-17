import setuptools

import scripts.configuration
import scripts.environment


environment_instance = scripts.environment.load_environment()
configuration_instance = scripts.configuration.load_configuration(environment_instance)
parameters = scripts.configuration.get_setuptools_parameters(configuration_instance)


resource_patterns = [
	'static/**/*.css',
	'static/**/*.js',
	'static/**/*.json',
	'static/**/*.jpg',
	'static/**/*.png',
	'static/resume.pdf',
	'templates/**/*.html',
]

parameters.update({
	"name": "bhamon-website",
	"description": "Website for Benjamin Hamon",
	"packages": [ "bhamon_website" ],
	"python_requires": "~= 3.5",
	"install_requires": [ "python-dateutil", "flask ~= 1.0" ],
	"package_data": { "bhamon_website": scripts.configuration.list_package_data("bhamon_website", resource_patterns) },
})

setuptools.setup(**parameters)
