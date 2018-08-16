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


def get_appropriate_seller_parse_fn(parser_id_num):
	module_name = 'parser_id_{}'.format(parser_id_num)
	try:
		appropriate_parser_module = import_module(
			'app.template_parsing.seller_patterns.{}.parse'.format(module_name))
	except ImportError:
		raise ImportError('Could not locate parser module')
	else:
		appropriate_parse_fn = appropriate_parser_module.parse
		return appropriate_parse_fn


def parse(json_input):
	start = json.loads(json_input)
	simple_preparse_response_check(start['response'])
	parser_fn = get_appropriate_seller_parse_fn(int(start['parser_id_num']))
	parsed_data = parser_fn(json.dumps(start['response']))
	return parsed_data.json()







