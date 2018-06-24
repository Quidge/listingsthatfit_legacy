from ebaysdk.exception import PaginationLimit
from sqlalchemy.orm.exc import NoResultFound
from app.models import Item, EbaySeller
from app import db


def compare_and_return_new_items(set_of_ebay_item_ids, ebay_seller_id=None):
	"""Compares a set of ebay item ids against a DB query and returns a set of items
	that are not represented in the db."""
	if ebay_seller_id is not None:
		try:
			seller = db.session.query(
				EbaySeller).filter(EbaySeller.ebay_seller_id == ebay_seller_id).one()
		except NoResultFound:
			raise NoResultFound('No seller found for <{}>'.format(ebay_seller_id))
		db_item_results = db.session.query(
			Item.ebay_item_id).filter(Item.seller == seller).all()
		db_set = set([i[0] for i in db_item_results])
		return set_of_ebay_item_ids - db_set
	else:
		db_item_results = db.session.query(Item.ebay_item_id).all()
		db_set = set([i[0] for i in db_item_results])
		return set_of_ebay_item_ids - db_set


def lookup_single_item(connection, ebay_item_id, with_description=False):
	payload = {'ItemID': ebay_item_id}
	if with_description:
		payload['IncludeSelector'] = 'Description'
	r = connection.execute('GetSingleItem', payload)
	return r


def depaginate_search_result(connection):
	"""Depaginates a Finding connection that has been executed with a payload.

	Returns
	-------
	result : dict
		{'searchResult' : [list of items]}
	"""
	try:
		connection.response.dict()['searchResult']['item']
	except KeyError:
		raise ValueError(
			'Connection response does not appear to have any items\nResponse:\n%r' % (
				connection.response.reply,))

	result = {'searchResult': []}
	proceed = True
	while proceed:
		for item in connection.response.dict()['searchResult']['item']:
			result['searchResult'].append(item)
		try:
			connection.next_page()
		except PaginationLimit:
			proceed = False
	return result

