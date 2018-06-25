from datetime import datetime
import decimal
from sqlalchemy.orm.exc import NoResultFound
from app.models import Item, MeasurementType, ItemMeasurementAssociation, EbaySeller
from app.template_parsing.utils import parse_html_for_measurements
from app.template_parsing.exception import UnsupportedClothingCategory, UnrecognizedMeasurement, UnsupportedParsingStrategy


def gather_measurement_models_from_html_desc(
	html_description,
	ebay_category_id,
	parser_file_num,
	parse_strategy='default'):
	"""Return a list of ItemMeasurementAssociation models, built from the
	html_description param. The item association on these models is unset.

	Design philosophy: the parser should not be required to know anything
	about the possible or proper database measurement type names. Because the parser
	is ignorant, it falls to the model building functions to discern what the parser
	reports back.

	Parameters
	----------
	html_description : str
	ebay_category_id : int
	parser_file_num : int
		This is the parser file id tied to an ebay seller in the db.

	Returns
	-------
	measurement_models : list
	"""
	'''try:
		assert ebay_category_id in MeasurementType.SUPPORTED_CATEGORIES_EBAY_VALUES.keys()
	except AssertionError:
		raise AttributeError(
			'Parsing for ebay_category_id <{}> not supported'.format(ebay_category_id))'''

	try:
		measurements_obj = parse_html_for_measurements(
			html_description, ebay_category_id,
			parser_file_num, parse_strategy=parse_strategy)
	except UnsupportedClothingCategory:
		raise
	except UnrecognizedMeasurement:
		raise
	except UnsupportedParsingStrategy:
		raise

	measurement_models = []

	# suits are special because they have pants waist and jacket waist
	# attribute names reported from the parser are prepended with either 'jacket_'
	# or 'pant_'
	'''if measurements_obj == 3001:
		for key, msmt_value in measurements_obj.items():
			cat_name = None
			attribute = None
			if key[:6] == 'jacket':
				cat_name = 'sportcoat'
				attribute = key[7:]
			elif key[:4] == 'pant':
				cat_name = 'pant'
				attribute = key[5:]

			association = build_item_measurement(
				clothing_cat_string_name=cat_name,
				attribute=attribute,
				measurement_value=msmt_value)
			measurement_models.append(association)
			# print(association)

	else:
		for key, msmt_value in measurements_obj.items():
			association = build_item_measurement(
				clothing_cat_string_name=cat_name,
				attribute=key,
				measurement_value=msmt_value)
			measurement_models.append(association)
			# print(association)'''

	for msmt in measurements_obj.measurements_list:
		association = build_item_measurement(
			clothing_cat_string_name=msmt.category,
			attribute=msmt.attribute,
			measurement_value=msmt.value)
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
		print(clothing_cat_string_name, attribute, measurement_value)
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

	Parameters
	----------
	single_item_response : dict
	ebay_seller_id : str
	with_measurements : bool
		If true, response will be searched for a description and measurement parsing
		for that description will be attempted.
	with_sizes : bool
		If true, response will be searched for a description and size parsing
		for that description will be attempted.
	affiliate_url = str or None

	Returns
	-------
	configured sqlalchemy app.models.Item model object
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
	m.last_access_date = datetime.strptime(
		single_item_response['Timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

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

		# This and the next try/except could possibly be combined?
		try:
			assert seller.template_parser != None
		except AssertionError:
			raise ValueError(
				'No template parser associated with <{}>'.format(seller.ebay_seller_id))

		try:
			parser_file_num = seller.template_parser.file_name_number
		except:
			raise
		measurement_models = gather_measurement_models_from_html_desc(
			html_desc, m.ebay_primary_category, parser_file_num)

		# damn, list comprehensions are cool
		try:
			[m.measurements.append(model) for model in measurement_models]
		except UnsupportedClothingCategory:
			raise

	return m


