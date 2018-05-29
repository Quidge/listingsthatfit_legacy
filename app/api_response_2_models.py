from app.models import Item, MeasurementType, ItemMeasurementAssociation, EbaySeller
from importlib import import_module
from sqlalchemy.orm.exc import NoResultFound


def build_item_from_response(
	single_item_response,
	item_description_present=False,
	item_seller_ebay_name_id=None,
	item_specifics_present=False):
	"""Maps a dictionary response from ebay getSingleItem API to an Item model class.

	Built to be a director for several smaller construct_Item_model functions determined
	by the clothing category. Which smaller function to use is determined by a big
	conditional (which is stupid). Neither this directory function or it's sub functions
	create entries in the DB.

	If either item_specifics_present or item_description_present are true, that means
	that the single_item_response dictrionary has entries for 'ItemSpecifics' and
	'Description' respectively.

	Important to note that a getSingleItem API response does not include information
	about the seller. The ebay seller id (which is a string, like 'balearic1') must
	be explicitely passed to this function.

	Returns an appropriately constructed Item model class instance.

	"""

	try:
		assert item_seller_ebay_name_id is not None
		# Get seller representation in the DB
		seller = EbaySeller.query.filter(EbaySeller.seller_id == item_seller_ebay_name_id).one()
	except AssertionError:
		# Seller ebay id not given to function. Should fail.
		raise
	except NoResultFound:
		# Seller doesn't exist in DB. Should fail.
		raise

	if item_description_present or item_specifics_present:
		try:
			# Import seller parsing module dynamically with importlib.import_module
			seller_parser_module = import_module('app.template_parsing.seller_id_{}'.format(seller.id))
		except ImportError:
			raise

	try:
		clothing_cat = single_item_response['Item']['PrimaryCategoryID']
	except KeyError:
		# Something must be wrong with the response given to the function. Should fail.
		raise

	if clothing_cat == 3002:
		item = build_sportcoat_item(
			single_item_response,
			item_description_present=item_description_present,
			item_specifics_present=item_specifics_present)
	else:
		raise BaseException('eBay item is not recognized')

	# Finally, associate the item with a seller
	item.seller = seller

	return item


def build_sportcoat_item(
	single_item_response,
	item_description_present=False,
	item_specifics_present=False):
	pass


def build_suit_item(
	single_item_response,
	item_description_present=False,
	item_specifics_present=False):
	pass


def build_shirt_dress_item(
	single_item_response,
	item_description_present=False,
	item_specifics_present=False):
	pass


def build_shirt_casual_item(
	single_item_response,
	item_description_present=False,
	item_specifics_present=False):
	pass


def build_pants_item(
	single_item_response,
	item_description_present=False,
	item_specifics_present=False):
	pass


def build_pants_item(
	single_item_response,
	item_description_present=False,
	item_specifics_present=False):
	pass
