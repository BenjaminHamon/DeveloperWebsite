import dateutil.parser


def render_text(value):
	return value if value is not None else ""


def render_date(value, format_spec):
	if value is None:
		return ""

	value = dateutil.parser.parse(value)
	return value.strftime(format_spec)
