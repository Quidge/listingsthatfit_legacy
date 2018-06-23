from ebaysdk.exception import ConnectionError, PaginationLimit
from ebaysdk.finding import Connection as Finding

from app.ebay2db.core import depaginate_search_result, compare_and_return_new_items


def lookup_and_add_new_items(
	connection,
	ebay_seller_id=None,
	payload_additions=None,
	custom_payload=None,
	use_affiliate=False):
	"""High level abstractin. Executes findingApi to retrieve list of all items for a
	a seller. From that list, a sub list of items that are not already held in the DB is constructed.
	Against this sub list, GetSingleItem is executed and models are built for those items.
	If possible, also constructs measurement and size models for each item and attaches
	them to the item model before committing.

	payload_additions will be appended to the payload sent to Finding API, and if
	duplicates are found* will overwrite those used in the default payload.

	*If they key in the tuple is 'itemFilter', the value will be appended to a list of
	itemFilters in the payload. It will not overwrite.

	Parameters
	----------
	connection : object
		configured ebaysdk Finding connection
	ebay_seller_id : str
		valid ebay_seller_id; ex: 'balearic1'
	payload_additions : list of tuples
		ex: ('categoryId', '3002')
	custom_payload : dict
		Overrides default payload sent to Finding connection
	use_affiliate : Boolean


	Returns
	-------
	None
	"""

	try:
		assert ebay_seller_id is not None
	except AssertionError:
		raise ValueError('ebay_seller_id not provided')

	# AFFILIATE LINKING NOT SUPPORTED
	if use_affiliate:
		raise ValueError('Affiliate linking is not supported at this time.')
	
	# PAYLOAD ADDITIONS NOT SUPPORTED
	if payload_additions is not None:
		raise ValueError('Payload additions not supported at this time')

	payload = {'itemFilter': [
			{'name': 'Seller', 'value': ebay_seller_id},
			{'name': 'listingType', 'value': 'Auction'}
		]
	}

	# Override payload if provided
	if custom_payload is not None:
		payload = custom_payload

	c = connection

	try:
		c.execute('findItemsAdvanced', payload)
	except ConnectionError:
		raise

	# Build up a depaginated list of item IDs from the result.
	all_items = depaginate_search_result(c)

	# For some reason, the connection returns duplicates. With the only parameters
	# being Seller='balearic1' and listingType='Auction', there are usually ~5-10 duplicates.
	# So, ~%1.
	# I believe this is a problem with ebaysdk, not that Spoo has duplicate listings.
	# But I can't have duplicate ebay item IDs, so those are going to be dropped until
	# I fix this bug.
	all_item_ids = [i['itemId'] for i in all_items]
	unique_item_ids = set(all_item_ids)
	if len(all_item_ids) - len(unique_item_ids) > 0:
		print('Duplicate items detected. Dropped: {} items.'.format(len(all_item_ids) - len(unique_item_ids)))

	
	return all_items


def update_all_db_items_price(connection):
	"""Updates current price for every item in db."""
	pass

# lookup_and_add_all_new_items(connection)


# items = lookup_and_add_new_items(fapi, 'balearic1')

#print(len(items), print(len(set(items))))




