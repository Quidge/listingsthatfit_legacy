from ebaysdk.exception import ConnectionError, ConnectionResponseError
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
