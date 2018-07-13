from app.instance import shopping_connection as sapi
from app.ebayapis.core.lookup import lookup_single_item
from app.model_builders import build_ebay_item_model


def build_item_model(ebay_item_id, ebay_seller_id=None, with_measurements=True):
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
		with_measurements=with_measurements)
	return m
