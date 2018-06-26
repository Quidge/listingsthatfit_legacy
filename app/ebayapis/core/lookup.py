def lookup_single_item(connection, ebay_item_id, with_description=False):
	"""Executes GetSingleItem method call to connection.

	Parameters
	----------
	connection : ebaysdk Shopping connection
	ebay_item_id : int
	with_description : bool

	Returns
	-------
	r : ebaysdk connection RESPONSE object
	"""
	payload = {'ItemID': ebay_item_id}
	if with_description:
		payload['IncludeSelector'] = 'Description'
	r = connection.execute('GetSingleItem', payload)
	return r


def get_auction_items_from_seller(connection, ebay_seller_id):
	"""Execute a findItemsAdvanced method call to the connection. Payload is
	configured to return Auction items for ebay_seller_id.

	Parameters
	----------
	connection : ebaysdk Finding connection
	ebay_seller_id : str

	Returns
	-------
	r : ebaysdk connection RESPONSE object
	"""

	r = connection.execute(
		'findItemsAdvanced',
		{'ItemFilter': [
			{'name': 'Seller', 'value': ebay_seller_id},
			{'name': 'listingType', 'value': 'Auction'}
		]
		}
	)
	return r
