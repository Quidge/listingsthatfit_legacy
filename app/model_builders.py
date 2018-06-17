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

	# print(measurements_dict)

	cat_name = MeasurementType.SUPPORTED_CATEGORIES_EBAY_VALUES[ebay_category_id]
	print(cat_name)

	measurement_models = []
	for key, value in measurements_dict.items():
		association = build_item_measurement(
			clothing_cat_string_name=cat_name,
			attribute=key,
			measurement_value=value)
		measurement_models.append(association)
		print(association)

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
	except NoResultFound as e:
		raise e

	try:
		association = ItemMeasurementAssociation(
			measurement_type=measurement_type,
			measurement_value=measurement_value)
	except BaseException:
		print('Item Measurement failed to associate')
		raise

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
		seller = EbaySeller.query.filter(EbaySeller.ebay_seller_id == ebay_seller_id).one()
	except AssertionError:
		raise ValueError('ebay_seller_id not provided')
	except NoResultFound:
		# Couldn't find seller in database. Should fail.
		raise NoResultFound(
			'No matching seller found for <{}> in the database'.format(ebay_seller_id))

	# All times from these responses are UTC
	# http://developer.ebay.com/devzone/Shopping/docs/CallRef/types/simpleTypes.html#dateTime

	m = Item()
	m.last_access_date = datetime.strptime(single_item_response['Timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

	r = single_item_response['Item']

	m.seller = seller
	m.ebay_item_id = int(r['ItemID'])
	m.end_date = datetime.strptime(r['EndTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
	m.ebay_title = r['Title']
	m.ebay_primary_category = int(r['PrimaryCategoryID'])
	m.current_price = int(decimal.Decimal(r['ConvertedCurrentPrice']['value']) * 100)
	m.ebay_url = r['ViewItemURLForNaturalSearch']
	m.ebay_affiliate_url = affiliate_url

	if with_measurements:
		try:
			html_desc = r['Description']
		except KeyError:
			raise KeyError('No HTML description found in response')
		measurement_models = gather_measurement_models_from_html_desc(
			html_desc, m.ebay_primary_category, seller.id)

		# damn, list comprehensions are cool
		[m.measurements.append(model) for model in measurement_models]

	return m


