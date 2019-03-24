__version__ = None


try:
	import bhamon_website.__metadata__

	__version__ = bhamon_website.__metadata__.__version__

except ImportError:
	pass
