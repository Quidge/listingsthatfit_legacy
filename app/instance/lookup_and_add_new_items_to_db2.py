import logging
from ebaysdk.exception import ConnectionError
from sqlalchemy.orm.exc import NoResultFound

from app.ebayapis.core.utils import depaginate_search_result
from app.ebayapis.core.lookup import lookup_single_item
from app.dbtouch import compare_and_return_new_items
from app.model_builders import build_ebay_item_model

from app.models import EbaySeller

logger = logging.getLogger(__name__)


def lookup_and_create_models_for_new_items(
	finding_connection,
	shopping_connection,
	db_connection,
	ebay_seller_id,
	finding_payload_override=None,
	use_affiliate=False,
	with_measurements=False):
	"""High level abstractin. Executes findingApi to retrieve list of all items for a
	a seller. From that list, a sub list of items that are not already held in the DB is
	constructed. Against this sub list, GetSingleItem is executed and models are built
	for those items. If possible, also constructs measurement and size models for each
	item and attaches them to the item model before committing.

	Defaults to returning only AUCTION listing types

	Returns
	-------
	None
	"""

	logger.info('Beginning mass lookup and addition.')

	logger.debug('Quering db for knowledge of ebay_seller_id={}'.format(ebay_seller_id))
	try:
		seller = db_connection.session.query(
			EbaySeller).filter(
			ebay_seller_id == ebay_seller_id).first()
	except NoResultFound:
		raise NoResultFound('No seller found in db for ebay_id: <{}>'.format(ebay_seller_id))
	logger.debug('Found seller={}'.format(seller))

	msmts_parser = seller.template_parser

	try:
		assert msmts_parser is not None
	except AssertionError:
		raise AssertionError('<{}> does not have an associated template parser in the db')

	fapi = finding_connection
	sapi = shopping_connection

	if finding_payload_override:
		logger.debug('Using parameter payload override: <{}>'.format(finding_payload_override))
		f_payload = finding_payload_override
	else:
		f_payload = {'itemFilter': [
			{'name': 'Seller', 'value': ebay_seller_id},
			{'name': 'listingType', 'value': 'Auction'}
		]}

	try:
		fapi.execute('findItemsAdvanced', f_payload)
	except ConnectionError:
		raise

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

	depaged = depaginate_search_result(fapi)
	all_items = [int(i['itemId']) for i in depaged['searchResult']]

	unique_all_items = set(all_items)

	unrecognized_in_db = compare_and_return_new_items(unique_all_items, ebay_seller_id)

	print(
		'Call to findItemsAdvanced returned <{}>. <{}> of those are unique.'.format(
		len(all_items), len(unique_all_items)))
	print('Of those unique items, will only attempt to add <{}>. The rest are already known about in the db.'.format(
		len(unrecognized_in_db)))

	sapi_lookups = []

	for item_id in unrecognized_in_db:
		try:
			res_dict = lookup_single_item(sapi, item_id, with_description=with_measurements).dict()
		except ConnectionError as e:
			print(
				'GetSingleItem call to Shopping connection failed for item: <{}>.'.format(item_id))
			raise e
		else:
			sapi_lookups.append(res_dict)

	logger.debug('Acquired a list of {} GetSingleItem calls.'.format(len(sapi_lookups)))

	ebay_item_models = []

	for item_res in sapi_lookups:
		i_id = item_res['Item']['ItemID']
		logger.info('Attempting to build model for item <{}>.'.format(i_id))

		# This could be sped up by resusing the same seller result each time.
		# Each time build_ebay_item_model searches the db for ebay_seller_id.

		try:
			m = build_ebay_item_model(
				item_res,
				ebay_seller_id=ebay_seller_id,
				attempt_parse=True)
		except NoResultFound as e:
			logger.exception('Found error. Skipping this item')
			continue

		if m is not None:
			logger.info('Built model for item <{}>'.format(m.ebay_item_id))
			ebay_item_models.append(m)
		else:
			logger.info('Failed to build model for item.')

	logger.info((
		'Model construction finished. '
		'<{}> Item models built.').format(len(ebay_item_models)))
	return ebay_item_models


if __name__ == '__main__':
	from app.instance import shopping_connection as s_api, finding_connection as f_api
	from app import db

	logger = logging.getLogger('app.instance.lookup_and_add_new_items_to_db2')
	logger.info('Running lookup_and_add_new_items_to_db2 as script')

	payload = {
		'itemFilter': [
			{'name': 'Seller', 'value': 'balearic1'},
			{'name': 'listingType', 'value': 'Auction'},
			{'name': 'ExcludeCategory', 'value': [
				4250, 15724, 93427, 179243, 4251, 169291, 3034, 171146, 155185, 11700, 11511]}
		],
		# 'categoryId': [3001]
	}
	# 4250 = Mens-Accessories
	# 15724 = Women's Clothing
	# 93427 = Men's Shoes
	# 179243 = Unisex Sunglasses & Sunglasses Accessories
	# 4251 = Women's Accessories
	# 169291 = Women's Bags & Handbags
	# 3034 = Women's Shoes
	# 171146 = Kids' Clothing, Shoes & Accessories
	# 155185 = Unisex Accessories
	# 11700 = Home & Garden
	# 11511 = Men's Socks

	models = lookup_and_create_models_for_new_items(
		f_api,
		s_api,
		db,
		'balearic1',
		finding_payload_override=payload,
		with_measurements=True)

	db.session.add_all(models)
	db.session.flush()
	db.session.commit()

	# print(lookup_and_add_new_items_to_db(f_api, s_api, db, 'balearic1'))











