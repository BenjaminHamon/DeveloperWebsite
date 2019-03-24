import logging


log_format = "[{levelname}][{name}] {message}"


def configure_logging(log_level):
	logging.basicConfig(level = log_level, format = log_format, style = "{")
	logging.addLevelName(logging.DEBUG, "Debug")
	logging.addLevelName(logging.INFO, "Info")
	logging.addLevelName(logging.WARNING, "Warning")
	logging.addLevelName(logging.ERROR, "Error")
	logging.addLevelName(logging.CRITICAL, "Critical")

	logging.getLogger("werkzeug").setLevel(logging.WARNING)
