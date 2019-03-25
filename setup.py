import setuptools

import scripts.configuration
import scripts.environment


environment_instance = scripts.environment.load_environment()
configuration_instance = scripts.configuration.load_configuration(environment_instance)
parameters = scripts.configuration.get_setuptools_parameters(configuration_instance)

parameters.update({
	"name": "bhamon-website",
	"description": "Website for Benjamin Hamon",
	"packages": [ "bhamon_website" ],
	"python_requires": "~= 3.5",
	"install_requires": [ "flask ~= 1.0" ],
})

setuptools.setup(**parameters)
