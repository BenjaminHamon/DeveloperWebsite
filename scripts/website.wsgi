import logging
import os
import platform

workspace = os.path.dirname(os.path.dirname(__file__))
venv_activation_file_path = workspace + "/.venv/bin/activate_this.py"
if platform.system() == "Windows":
    venv_activation_file_path = workspace + "/.venv/scripts/activate_this.py"
with open(venv_activation_file_path) as venv_activation_file:
    exec(venv_activation_file.read(), dict(__file__ = venv_activation_file_path))


import scripts.environment
import scripts.website

scripts.environment.configure_logging(logging.INFO)
logging.getLogger("Request").setLevel(logging.WARNING)
application = scripts.website.create_application()
