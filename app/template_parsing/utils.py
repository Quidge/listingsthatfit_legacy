import re
from importlib import import_module
from decimal import Decimal

from app.template_parsing.exception import UnsupportedClothingCategory
from app.ebay2db import ebay_clothing_categories


def parse_html_for_measurements(
	item_html_description,
	clothing_category_id,
	parser_file_id_num,
	parse_strategy='default'):
	"""Takes html_description and seller_id number and returns a dictionary object of
	measurements.

	Parameters
	----------
	item_html_description : str
	clothing_category_id : int
	parser_file_id_num : int
	parse_strategy : str
		This will be handed down to the individual parser file

	Returns
	-------
	measurements_obj : MeasurementsCollection instance
	"""

	try:
		module_name = 'parser_id_{}'.format(parser_file_id_num)
		measurements_parser = import_module(
			'app.template_parsing.seller_patterns.{}'.format(module_name))
	except ImportError:
		raise

	"""
	If a parser (for a clothing category) has been written, it will be included in a
	module 'directory' that is a dict with category ids key-ed to functions
		ie: {3001: get_suit_measurements}
	"""
	if clothing_category_id not in measurements_parser.function_directory:
		raise UnsupportedClothingCategory(
			'Parser file for file <{}> does not support parsing for category <{}>'.format(
				module_name, clothing_category_id))

	category_parser = measurements_parser.function_directory[clothing_category_id]

	# measurements_obj is an instance of MeasurementsCollection
	measurements_obj = category_parser(
		item_html_description, parse_strategy=parse_strategy)
	# measurements_obj doesn't come back with the clothing cat string name configured
	measurements_obj.clothing_category_name = ebay_clothing_categories[clothing_category_id]

	return measurements_obj


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
	match = re.search(digit_pattern, string_measurement_value)
	if match is None:
		return None
	decimal_string = match.group(0)
	return int(Decimal(decimal_string) * 1000)





