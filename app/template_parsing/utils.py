import re
from importlib import import_module
from decimal import Decimal


def parse_html_for_measurements(
	item_html_description,
	clothing_category_id,
	parser_file_id_num):
	"""Takes html_description and seller_id number and returns a dictionary object of
	measurements.

	Parameters
	----------
	item_html_description : str
	category_id : int
	seller_id_num : int

	Returns
	-------
	item_sizes : dict
		In form:
			{
				"chest": 23000,
				"shoulders": 19375,
				... ,
				etc
			}
	"""
	try:
		module_name = 'parser_id_{}'.format(parser_file_id_num)
		measurements_parser = import_module('app.template_parsing.seller_patterns.{}'.format(module_name))
	except ImportError:
		raise

	if clothing_category_id == 3002:
		return measurements_parser.get_sportcoat_measurements(item_html_description)
	# elif clothing_category_id == other numbers
		# return measurements_parser.other_item_parsers
	else:
		raise AttributeError(
			'Unable to parse items in category <{}>'.format(clothing_category_id))

	return None

def find_paired_measurement_value(navigable_str):
	"""Returns first(!) string measurement value '22.5"' that is found in the
	same row as navigable string."""
	row = navigable_str.parent.parent  # str > td > tr
	row_strs = row.stripped_strings
	for s in row_strs:
		str_decimal = re.search(re.compile('\d*\.?\d\"'), s)  # .75" or 33" or 33.75"
		if str_decimal != None:
			return str_decimal.group(0)  # should return first measurement value string found


def str_measurement_to_int(string_measurement_value):
	"""Uses regex pattern \[\d.]+\ to find first instance of a decimal number.
	Converts that string instance to a Decimal, multiplies by 1000, and converts to an
	Integer. Returns the Integer.

	Parameters
	----------
	string_measurement_value : str

	Returns
	-------
	decimal : Decimal

	"""
	digit_pattern = re.compile('[\d.]+')
	decimal_string = re.search(digit_pattern, string_measurement_value).group(0)
	return int(Decimal(decimal_string) * 1000)





