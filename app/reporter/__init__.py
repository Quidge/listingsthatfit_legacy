import logging
from jinja2 import Environment, PackageLoader

logger = logging.getLogger(__name__)

reporter_jinja_env = Environment(
	loader=PackageLoader('app.reporter', 'templates')
)


def datetimeformat(value, format_str='%H:%M / %d-%m-%Y'):
	return value.strftime(format_str)


def int2inch_str(value, format_str='eigth'):
	"""Expects integers as multiples of 1000. Divides these by 1000, turns the result to 
	a str and appends a '"' (double quote) to that string. Returns that string."""
	if format_str == 'eigth':
		return '{}"'.format(int(value) / 1000)
	else:
		raise ValueError('Format string <{}> not understood'.format(format_str))


reporter_jinja_env.filters['datetimeformat'] = datetimeformat
reporter_jinja_env.filters['int2inch_str'] = int2inch_str
