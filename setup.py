import setuptools

import development.configuration
import development.environment


environment_instance = development.environment.load_environment()
configuration_instance = development.configuration.load_configuration(environment_instance)
parameters = development.configuration.get_setuptools_parameters(configuration_instance)


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
	"package_data": { "bhamon_website": development.configuration.list_package_data("bhamon_website", resource_patterns) },
})

setuptools.setup(**parameters)
