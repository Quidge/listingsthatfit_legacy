import logging
from app.instance import shopping_connection as sapi
from app.ebayapis.core.lookup import lookup_single_item
from app.model_builders import build_ebay_item_model

logger = logging.getLogger(__name__)


def build_item_model(
	ebay_item_id, ebay_seller_id=None, with_measurements=True,
	measurement_parse_strategy='default'):
	"""Attempts to construct an Item instance (and parse for ItemMeasurements) for an
	item.

	Parameters
	----------
	ebay_item_id : int
	ebay_seller_id : str
	with_measurements : boolean (defaults to True)

	Returns
	-------
	m : Item instance
	"""

	logger.info((
		'Attempting to build item model. ebay_item_id={}, ebay_seller_id={}, '
		'with_measurements={}, parse_strategy={}').format(
		ebay_item_id, ebay_seller_id, with_measurements, measurement_parse_strategy))
	try:
		assert ebay_seller_id is not None
	except AssertionError:
		raise ValueError('Expected ebay_seller_id as str. Got <{}>'.format(ebay_seller_id))
	logger.debug('Running lookup_single_item')
	res_dict = lookup_single_item(
		sapi, ebay_item_id,
		with_description=with_measurements).dict()
	logger.debug('lookup_single_item acquired a response dict.')
	logger.debug('Passing response dict and other parameters to build_ebay_item_model.')
	m = build_ebay_item_model(
		res_dict,
		ebay_seller_id=ebay_seller_id,
		attempt_parse=with_measurements,
		measurement_parse_strategy=measurement_parse_strategy)
	logger.info('Built item model successfully.')
	return m


if __name__ == '__main__':
	import logging
	from app import db

	logger = logging.getLogger('app.instance.build_item_model')
	print('Running build_item_model in script mode (where name is __main__)')

	m = build_item_model(362410421416, ebay_seller_id='balearic1')
	print(type(m.ebay_title), m.ebay_title)
	print(type(m.end_date), m.end_date)
	print(type(m.ebay_item_id), m.ebay_item_id)
	print(type(m.last_access_date), m.last_access_date)
	print(type(m.current_price), m.current_price)
	print(type(m.primary_category_number), m.primary_category_number)
	print(m.seller)
	print(type(m.assigned_clothing_category), m.assigned_clothing_category)
	for msmt in m.measurements:
		print(msmt)



