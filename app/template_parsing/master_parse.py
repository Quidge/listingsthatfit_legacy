import logging
import json
from importlib import import_module

from app.template_parsing.exception import UnsupportedClothingCategory

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


def get_appropriate_seller_parse_module(parser_id_num):
	"""Takes a parser id number and returns the appropriate parsing package.
	Raises ImportError if parsing module cannot be found."""
	module_name = 'parser_id_{}'.format(parser_id_num)
	try:
		appropriate_parser_module = import_module(
			'app.template_parsing.seller_patterns.{}.parse'.format(module_name))
	except ImportError:
		raise ImportError('Could not locate parser module')
	else:
		return appropriate_parser_module


def parse(json_str):
	"""Highest level parsing function. Takes json data in and returns json.

	Parameters
	----------
	json_str : json str
		expected to be in form '{
			"parse_strategy": "default",
			"parser_id_num": some_number,
			"response": { GetSingleItem shopping API call, WITH description HTML }
			}
		}'

		Returns
		-------
		parsed_data : json encoded ParseResult instance
		"""

	start = json.loads(json_str)
	simple_preparse_response_check(start['response'])
	# parser_fn = get_appropriate_seller_parse_fn(int(start['parser_id_num']))
	parser_module = get_appropriate_seller_parse_module(int(start['parser_id_num']))
	# parsed_data = parser_fn(json.dumps(start['response']))
	parsed_data = parser_module.parse(json.dumps(start['response']))
	return parsed_data.json()







