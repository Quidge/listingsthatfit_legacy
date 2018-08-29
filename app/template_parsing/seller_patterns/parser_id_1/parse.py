import logging
import json
from .core.director import director
from .core.get_measurements_table import get_measurements_table
from .core.identify_clothing_type import identify_clothing_type
from app.template_parsing import ParseResult
from app.template_parsing.exception import (
	TemplateParsingError, UnsupportedClothingCategory, UnrecognizedMeasurement,
	UnrecognizedTemplateHTML)

logger = logging.getLogger(__name__)


def simple_preparse_response_check(r_dict):
	"""Quick check to be sure that the response Ack=Success and atleast has 'Item',
	Item['Description'] and Item['PrimaryCategoryID'] keys."""

	logger.debug('Running preparse check on response')
	try:
		assert r_dict['Ack'] == 'Success'
	except AssertionError:
		raise ValueError('Invalid response. Ack indicates failure')
	except KeyError:
		raise KeyError('Invalid response. Ack attribute not present')

	try:
		assert 'Item' in r_dict
	except AssertionError:
		raise KeyError('Invalid response. No Item attribute')

	try:
		assert 'Description' in r_dict['Item']
	except AssertionError:
		raise KeyError('Invalid response. Description attribute not present')

	try:
		assert 'PrimaryCategoryID' in r_dict['Item']
	except AssertionError:
		raise KeyError('Invalid response. PrimaryCategoryID attribute not present')

	logger.debug('Response dict passed simple preparse check')


def parse(json_str):
	"""Parser for spoo

	Parameters
	----------
	json_str : str
		Expects raw api json response from ebay Shopping GetSingleItem call

	Returns
	-------
	parse_result : ParseResult instance
	"""

	r = json.loads(json_str)

	simple_preparse_response_check(r)

	logger.info('Beginning parse')

	parse_result = ParseResult()

	measurements_table_soup = get_measurements_table(
		r['Item']['Description'], output_fmt='soup')
	ebay_primary_cat_id = int(r['Item']['PrimaryCategoryID'])
	identify_result = identify_clothing_type(
		measurements_table_soup,
		ebay_primary_category_id=ebay_primary_cat_id)

	parse_result.meta = {
		'parse_strategy': 'default',
		'concerns': identify_result.concerns,
		'parsed_html': identify_result.html_used_to_make_observations}
	parse_result.clothing_type = identify_result.identified_clothing_type
	parse_result.measurements = []

	# shortcircuit if result is None. parsing is useless at this point.
	if parse_result.clothing_type is None:
		return parse_result

	# shortcircuit if appropriate parse function cannot be found. This case should only be
	# programmer error. Identify should only return non None string names for clothing that the
	# director is able to recognize.
	try:
		parse_fn = director(identify_result.identified_clothing_type)
	except UnsupportedClothingCategory:
		logger.exception(
			'Identify returned a clothing type that the director did not now about')
		return parse_result

	try:
		logger.debug('Attempting to parse using {}'.format(parse_fn.__name__))
		msmts_collection = parse_fn(
			measurements_table_soup, parse_strategy='default')
	except UnrecognizedMeasurement:
		logger.exception('The parse function <{}> had difficulty with one of the measurements')
		return parse_result  # return with empty measurements
	except UnrecognizedTemplateHTML:
		logger.exception('The parse function <{}> had difficulty recogizing the template HTML')
		return parse_result  # return with empty measurements

	parse_result.measurements = msmts_collection.measurements_list
	logger.info('Successfully completing parsing parsing')

	return parse_result
