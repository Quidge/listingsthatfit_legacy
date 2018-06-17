from ebaysdk.exception import ConnectionError, ConnectionResponseError
from craywatch import finding_connection as f_api


def request_completed(
	ebay_seller='balearic1',
	category_id=None):
	"""Returns completed results from findCompletedItems.

	Parameters
	----------
	ebay_seller='balearic1'
	category_id=None

	Returns
	-------
	r : response object
	"""

	payload = {
		'itemFilter': {'name': 'Seller', 'value': ebay_seller}
	}
	if category_id is not None:
		payload['categoryId'] = category_id

	try:
		r = f_api.execute('findCompletedItems', payload)
	except ConnectionError:
		raise

	try:
		assert r.dict()['ack'] == 'Success'
	except AssertionError:
		raise ConnectionResponseError(r.dict()['errorMessage'], response=r)

	return f_api
