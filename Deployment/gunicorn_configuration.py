# cspell:words levelname

import multiprocessing

from benjaminhamon_standard_extensions.logging import logging_helpers


wsgi_app = "benjaminhamon_developer_website.wsgi_entry_point"

workers = multiprocessing.cpu_count() * 2 + 1

logconfig_dict = {
	"version": 1,

	"root": {
	    "level": "DEBUG",
	    "handlers": [ "stdout" ],
	},

	"loggers": {
	    "gunicorn.error": {
	        "level": "INFO",
	        "propagate": True,
	    },
	},

	"handlers": {
	    "stdout": {
	        "class": "logging.StreamHandler",
	        "formatter": "generic",
	        "stream": "ext://sys.stdout",
	    },
	},

	"formatters": {
	    "generic": {
	        "style": "{",
	        "format": "{asctime} [{levelname}][{name}] ({process}) {message}",
	        "datefmt": logging_helpers.date_format_iso,
	        "class": "logging.Formatter",
	    }
	}
}
