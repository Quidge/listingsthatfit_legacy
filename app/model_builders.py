from app.models import Item, MeasurementType, ItemMeasurementAssociation, EbaySeller
from app.template_parsing import utils
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
import decimal


def gather_measurement_models_from_html_desc(
	html_description,
	ebay_category_id,
	internal_seller_id):
	"""Return a list of ItemMeasurementAssociation models, built from the
	html_description param. The item association on these models is unset.
	
	Parameters
	----------
	html_description : str
	ebay_category_id : int
	internal_seller_id : int
		This is the primary id for an entry in the ebay_sellers table.

	Returns
	-------
	measurement_models : list
	"""
	try:
		assert ebay_category_id in MeasurementType.SUPPORTED_CATEGORIES_EBAY_VALUES.keys()
	except AssertionError:
		raise AttributeError(
			'Parsing for ebay_category_id <{}> not supported'.format(ebay_category_id))

	measurements_dict = utils.parse_html_for_measurements(
		html_description, ebay_category_id, internal_seller_id)

	cat_name = MeasurementType.SUPPORTED_CATEGORIES_EBAY_VALUES[ebay_category_id]

	measurement_models = []
	for key, value in measurements_dict.items():
		association = build_item_measurement(
			clothing_cat_string_name=cat_name,
			attribute=key,
			measurement_value=value)
		measurement_models.append(association)

	return measurement_models


def build_item_measurement(
	clothing_cat_string_name=None,
	attribute=None,
	measurement_value=None):

	try:
		assert clothing_cat_string_name is not None
		assert attribute is not None
		assert measurement_value is not None
	except AssertionError:
		raise
	try:
		measurement_type = MeasurementType.query.filter(
			MeasurementType.clothing_category == clothing_cat_string_name,
			MeasurementType.attribute == attribute).one()
	except NoResultFound:
		raise

	association = ItemMeasurementAssociation(
		measurement_type=measurement_type,
		measurement_value=measurement_value)

	return association


def build_ebay_item_model(
	single_item_response,
	ebay_seller_id=None,
	with_measurements=False,
	with_sizes=False,
	affiliate_url=None):
	"""Takes an ebay_seller_id, and GetSingleItem ebay API response, and affiliate_url
	(if provided) and returns a appropriately configured Item model.
	"""

	try:
		assert ebay_seller_id is not None
		seller = EbaySeller.query.filter(EbaySeller.seller_id == ebay_seller_id).one()
	except AssertionError:
		raise ValueError('ebay_seller_id not provided')
	except NoResultFound:
		# Couldn't find seller in database. Should fail.
		raise

	# All times from these responses are UTC
	# http://developer.ebay.com/devzone/Shopping/docs/CallRef/types/simpleTypes.html#dateTime

	m = Item()
	m.last_access_date = datetime.strptime(single_item_response['Timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

	r = single_item_response['Item']

	m.seller = seller
	m.ebay_item_id = int(r['ItemID'])
	m.end_date = datetime.strptime(r['EndTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
	m.ebay_title = r['Title']
	m.ebay_primary_category_id = int(r['PrimaryCategoryID'])
	m.current_price = int(decimal.Decimal(r['ConvertedCurrentPrice']['value']) * 100)
	m.ebay_url = r['ViewItemURLForNaturalSearch']
	m.ebay_affiliate_url = affiliate_url

	'''if with_measurements and getattr(r, 'Description', None) is not None:
		try:
			clothing_cat_ebay_id = int(r['PrimaryCategoryID'])
			assert clothing_cat_ebay_id in MeasurementType.SUPPORTED_EBAY_VALUES.keys()
		except AssertionError:
			raise BaseException(
				'eBay category <{}> not supported for parsing'.format(clothing_cat_ebay_id))

		measurements_dict = utils.parse_html_for_measurements(
			r['Description'], clothing_cat_ebay_id, seller.id)
		for key, value in measurements_dict.items():
			association_model = build_item_measurement(
				clothing_cat_string_name=MeasurementType.SUPPORTED_EBAY_VALUES[clothing_cat_ebay_id],
				attribute=key,
				measurement_value=value)
			m.measurements.append(association_model)
	'''

	if with_measurements:
		try:
			html_desc = r['Description']
		except KeyError:
			raise KeyError('No HTML description found in response')
		measurement_models = gather_measurement_models_from_html_desc(
			html_desc, m.ebay_primary_category_id, seller.id)

		# damn, list comprehensions are cool
		[m.measurements.append(model) for model in measurement_models]

	return m



'''class EbayItem(object):

	def __init__(self, generation_dict, item_seller_name_id=None):
		self.generation_dict = generation_dict
		self.seller_ebay_id = item_seller_name_id

		try:
			self.html_description = generation_dict['Item']['Description']
		except KeyError:
			self.html_description = None
		self.measurements = None

		try:
			self.item_specifics = generation_dict['Item']['ItemSpecifics']
		except KeyError:
			self.item_specifics = None
		self.sizes = None

		self.item_model = Item()

	def scrape_html_description_for_measurements(self):
		"""Parses html description for measurements. Returns parsed measurements as
		dict."""
		if self.html_description is None:
			raise ValueError('This instance has no html description to parse')
		if self.seller_ebay_id is None:
			raise ValueError("""Because this ebay_seller_id is 'None', this instance does
									know how to parse the html_description""")

		# Assert that it is known how to parse this ebay_category
		try:
			# 3002: sportcoat
			clothing_category = int(generation_dict['Item']['PrimaryCategoryID'])
			assert clothing_category in [3002]
		except AssertionError:
			raise ValueError(
				'PrimaryCategoryID is not recognizable: <{}>'.format(clothing_category))

		try:
			seller = EbaySeller.query.filter(EbaySeller.seller_id == self.seller_ebay_id).one()
		except NoResultFound:
			raise ValueError("<{}> could not be found in the database.".format(self.seller_ebay_id))

		try:
			module_name = 'app.template_parsing.seller_id_{}'.format(seller.id)
			parsing_tools = import_module(module_name)
		except ImportError:
			raise ImportError('Could not find parsing module: <{}>'.format(module_name))

		try:
			if clothing_category == 3002:
				self.measurements = parsing_tools.get_sportcoat_measurements(self.html_description)

			# Finally, return the measurements in addition to setting them internally.
			return self.measurements

		except ImportError:
			raise ImportError(
				'Cannot find correct method in <{}> for category <{}>'
				.format(parsing_tools, clothing_category))




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

	return item'''


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


