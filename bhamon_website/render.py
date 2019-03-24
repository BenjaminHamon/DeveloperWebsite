import datetime


def render_text(value):
	return value if value is not None else ""


def render_date(value, format_spec):
	if value is None:
		return ""

	value = datetime.datetime.fromisoformat(value)
	return value.strftime(format_spec)
