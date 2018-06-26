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

