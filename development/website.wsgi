import logging
import os
import platform
import sys

workspace = os.path.dirname(os.path.dirname(__file__))
venv_activation_file_path = os.path.join(workspace, ".venv", "Scripts" if platform.system() == "Windows" else "bin", "activate_this.py")
script_directory = os.path.join(workspace, "scripts")

with open(venv_activation_file_path) as venv_activation_file:
	exec(venv_activation_file.read(), dict(__file__ = venv_activation_file_path)) # pylint: disable = exec-used
sys.path.insert(0, script_directory)


import development.environment # pylint: disable = wrong-import-position
import development.website # pylint: disable = wrong-import-position

environment_instance = development.environment.load_environment()
development.environment.configure_logging(environment_instance, None)

logging.getLogger("werkzeug").setLevel(logging.WARNING)
logging.getLogger("Request").setLevel(logging.WARNING)

application = development.website.create_application()
