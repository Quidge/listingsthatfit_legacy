from ebaysdk.exception import ConnectionError, ConnectionResponseError, PaginationLimit
from craywatch import finding_connection as f_api


def request_items(
	min_price=None,
	min_bids=None,
	ebay_seller='balearic1',
	as_json=False,
	category_id=None):
	payload = {
		'itemFilter': [
			{'name': 'Seller', 'value': ebay_seller},
			{'name': 'listingType', 'value': 'Auction'},
			{'name': 'MinBids', 'value': min_bids},
			{'name': 'MinPrice', 'value': min_price}
		]
		# 'itemFilter': {'name': 'MinBids', 'value': min_bids}
		# 'itemFilter': {'name': 'MinPrice', 'value': min_price}
	}
	if category_id is not None:
		payload['categoryId'] = category_id

	try:
		r = f_api.execute('findItemsAdvanced', payload)
	except ConnectionError:
		raise

	try:
		assert r.dict()['ack'] == 'Success'
	except AssertionError:
		raise ConnectionResponseError(r.dict()['errorMessage'], response=r)

	if as_json:
		return r.json()
	else:
		return r.dict()


def return_executed_call_for_category(
	connection,
	category_id,
	min_price=None,
	min_bids=None,
	ebay_seller='balearic1'):
	payload = {
		'itemFilter': [
			{'name': 'Seller', 'value': ebay_seller},
			{'name': 'listingType', 'value': 'Auction'}
		],
		'categoryId': category_id
	}
	if min_bids is not None:
		payload['itemFilter'].append({'name': 'MinBids', 'value': min_bids})
	if min_price is not None:
		payload['itemFilter'].append({'name': 'MinPrice', 'value': min_price})

	try:
		r = connection.execute('findItemsAdvanced', payload)
	except ConnectionError:
		raise

	return {'response': r, 'connection': connection}


def depaginate_item_search_results(connection):
	"""Paginates through a connection that holds a response to concatonate
	a list of all items."""

	result = []
	proceed = True
	while proceed:
		try:
			for item in connection.response.dict()['searchResult']['item']:
				result.append(item)
		except KeyError:
			raise KeyError(connection.response.dict())
		try:
			connection.next_page()
		except PaginationLimit:
			proceed = False
	return result






