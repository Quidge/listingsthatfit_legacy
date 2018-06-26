from json import loads

from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding

# from app.model_builders import build_ebay_item_model
from app.template_parsing.exception import TemplateParsingError

ebay_clothing_categories = {
	3002: 'sportcoat',
	57991: 'dress_shirt',
	57990: 'casual_shirt',
	15662: 'tie',
	11484: 'sweater',
	57988: 'coats_and_jacket',
	57989: 'pant',
	11483: 'jeans',
	3001: 'suit',
	15691: 'vest',
	11510: 'sleepwear_and_robe',
	15690: 'swimwear',
	53120: 'dress_shoes'}


'''def lookup_and_add_new_items(
	finding_connection,
	shopping_connection,
	ebay_seller_id=None,
	payload_additions=None,
	custom_payload=None,
	use_affiliate=False,
	with_measurements=False,
	with_sizes=False):
	"""High level abstractin. Executes findingApi to retrieve list of all items for a
	a seller. From that list, a sub list of items that are not already held in the DB is
	constructed. Against this sub list, GetSingleItem is executed and models are built
	for those items. If possible, also constructs measurement and size models for each
	item and attaches them to the item model before committing.

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
		raise ValueError('Payload additions not supported at this time.')

	# SIZE PARSING NOT SUPPORTED
	if with_sizes:
		raise ValueError('Size parsing of items is not supported at this time.')

	payload = {'itemFilter': [
			{'name': 'Seller', 'value': ebay_seller_id},
			{'name': 'listingType', 'value': 'Auction'}
		]
	}

	# Override payload if provided
	if custom_payload is not None:
		payload = custom_payload

	f_conn = finding_connection

	try:
		f_conn.execute('findItemsAdvanced', payload)
	except ConnectionError:
		raise
	# Build up a depaginated list of item IDs from the result.
	all_items = depaginate_search_result(f_conn)

	# For some reason, the connection returns duplicates. With the only parameters
	# being Seller='balearic1' and listingType='Auction', there are usually ~5-10 duplicates.
	# So, ~%1.
	# I believe this is a problem with ebaysdk, not that Spoo has duplicate listings.
	# But I can't have duplicate ebay item IDs, so those are going to be dropped until
	# I fix this bug.

	"""
	2018/06/24 Update: I'm quite certain that ebay is returning duplicate entries. To prove:
	searchResult = all_items['searchResult']
	dup_dict = dict()
	for item in searchResult:
		item_id = item['itemId']
		if item_id in dup_dict:
			dup_dict[item_id].append(item)
		else:
			dup_dict[item_id] = [item]
	for _, stuff in dup_dict.items():
		if len(stuff) > 1:
			[print(i) for i in stuff]
	"""
	unique_item_ids = set([int(i['itemId']) for i in all_items['searchResult']])
	paginationOutput = f_conn.response.dict()['paginationOutput']['totalEntries']
	print('TotalEntries reported: <{}>, uniques: <{}>'.format(
		paginationOutput, len(unique_item_ids)))

	new_items = compare_and_return_new_items(unique_item_ids, ebay_seller_id=ebay_seller_id)
	new_item_models = []
	for ebay_id in new_items:
		try:
			res = lookup_single_item(
				shopping_connection, ebay_id, with_description=with_measurements)
		except ConnectionError:
			raise
		try:
			model = build_ebay_item_model(
				res.dict(),
				ebay_seller_id=ebay_seller_id,
				with_measurements=with_measurements,
				with_sizes=with_sizes)
		except TemplateParsingError:
			# Don't add items whose measurements cannot be parsed.
			pass
		else:
			new_item_models.append(model)
	return new_item_models'''





def update_all_db_items_price(connection):
	"""Updates current price for every item in db."""
	pass

# lookup_and_add_all_new_items(connection)


# items = lookup_and_add_new_items(fapi, 'balearic1')

#print(len(items), print(len(set(items))))




