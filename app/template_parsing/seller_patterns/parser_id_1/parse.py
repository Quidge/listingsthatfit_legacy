import logging
import json
from .core.director import director
from .core.get_measurements_table import get_measurements_table
from .core.identify_clothing_type import identify_clothing_type
from app.template_parsing import ParseResult

logger = logging.getLogger(__name__)


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

	logger.info('Beginning parse')

	r = json.loads(json_str)
	measurements_table_soup = get_measurements_table(
		r['Item']['Description'], output_fmt='soup')
	ebay_primary_cat_id = int(r['Item']['PrimaryCategoryID'])
	identify_result = identify_clothing_type(
		measurements_table_soup,
		ebay_primary_category_id=ebay_primary_cat_id)
	parse_fn = director(identify_result.identified_clothing_type)
	msmts_collection = parse_fn(
		measurements_table_soup, parse_strategy='default')

	parse_result = ParseResult()

	parse_result.meta = {
		'parse_strategy': 'default',
		'concerns': identify_result.concerns,
		'parsed_html': identify_result.html_used_to_make_observations}
	parse_result.clothing_type = identify_result.identified_clothing_type
	parse_result.measurements = [m.__dict__ for m in msmts_collection.measurements_list]

	return parse_result
