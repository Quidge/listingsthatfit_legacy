from app.instance import shopping_connection as sapi
from app.ebayapis.core.lookup import lookup_single_item
from app.model_builders import build_ebay_item_model, build_ebay_item_model2


def build_item_model(ebay_item_id, ebay_seller_id=None, with_measurements=True, measurement_parse_strategy='default'):
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

	try:
		assert ebay_seller_id is not None
	except AssertionError:
		raise ValueError('Expected ebay_seller_id as str. Got <{}>'.format(ebay_seller_id))
	res_dict = lookup_single_item(
		sapi, ebay_item_id,
		with_description=with_measurements).dict()
	m = build_ebay_item_model(
		res_dict,
		ebay_seller_id=ebay_seller_id,
		with_measurements=with_measurements,
		measurement_parse_strategy=measurement_parse_strategy)
	return m


def build_item_model2(ebay_item_id, ebay_seller_id=None, with_measurements=True, measurement_parse_strategy='default'):
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

	try:
		assert ebay_seller_id is not None
	except AssertionError:
		raise ValueError('Expected ebay_seller_id as str. Got <{}>'.format(ebay_seller_id))
	res_dict = lookup_single_item(
		sapi, ebay_item_id,
		with_description=with_measurements).dict()
	m = build_ebay_item_model2(
		res_dict,
		ebay_seller_id=ebay_seller_id,
		attempt_parse=with_measurements,
		measurement_parse_strategy=measurement_parse_strategy)
	return m


if __name__ == '__main__':
	m = build_item_model2(362410421416, ebay_seller_id='balearic1')
	print(m.ebay_title)
	print(m.ebay_item_id)
	print(m.end_date)
	print(m.primary_item_category)
	print(m.seller)
	print(m.assigned_clothing_category)
	for msmt in m.measurements:
		print(msmt)



