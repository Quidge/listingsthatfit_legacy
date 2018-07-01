from datetime import datetime
import decimal
from sqlalchemy.orm.exc import NoResultFound
from app.models import Item, EbaySeller, EbayItemCategory
from app.models import UserMeasurementPreference, MeasurementItemType, MeasurementItemCategory, ItemMeasurement
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
	"""Constructs and returns an appropriate ItemMeasurement instance.

	Parameters
	----------
	measurement_value : int
	clothing_cat_string_name : str
		Expected to match some MeasurementItemCategory.category_name record
	attribute : str
		Expected to match some MeasurementItemType.type_name record

	Returns
	-------
	association : ItemMeasurement instance
	"""

	try:
		assert clothing_cat_string_name is not None
		assert attribute is not None
		assert measurement_value is not None
	except AssertionError:
		print(clothing_cat_string_name, attribute, measurement_value)
		raise
	try:
		measurement_type = MeasurementItemType.query.filter(
			MeasurementItemType.type_name == attribute).one()
		measurement_category = MeasurementItemCategory.query.filter(
			MeasurementItemCategory.category_name == clothing_cat_string_name)
		'''measurement_type = MeasurementType.query.filter(
			MeasurementType.clothing_category == clothing_cat_string_name,
			MeasurementType.attribute == attribute).one()'''
	except NoResultFound as e:
		raise e

	try:
		association = ItemMeasurement(
			measurement_value=measurement_value,
			measurement_type=measurement_type,
			measurement_category=measurement_category)
		'''association = ItemMeasurementAssociation(
			measurement_type=measurement_type,
			measurement_value=measurement_value)'''
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

	primary_category = EbayItemCategory.query.filter(
		EbayItemCategory.category_number == int(r['PrimaryCategoryID'])).one()

	m.seller = seller
	m.ebay_item_id = int(r['ItemID'])
	m.end_date = datetime.strptime(r['EndTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
	m.ebay_title = r['Title']
	m.primary_item_category = primary_category
	# m.ebay_primary_category = int(r['PrimaryCategoryID'])
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


def build_user_measurement_preferences_for_ebay_item_category(
	ebay_item_category_object, user_object, db_conn, msmt_dict):
	"""Returns a list of UserMeasurementPreference models that can be constructed from
	the parameters and msmt_dict.

	Parameters
	----------
	ebay_item_category_object : EbayItemCategory instance
	user_object : User instance
	db_conn : db connection
	msmt_dict : dict
		in form {
			'jacket': {
				'sleeve': {'measurement': 2400, 'tolerance': 1000},
				'shoulders': {'measurement': 1850, 'tolerance': 500},
				...
				},
			...
			'pant': {
				'inseam': {'measurement': 31500, 'tolerance': '500'},
				...
				}
			}

	Returns
	-------
	pref_models : list
		A list of the UserMeasurementPreference instances that could be constructed
	"""
	pref_models = []
	sess = db_conn.session

	for msmt_category_name, msmt_type_dict in msmt_dict.items():
		for msmt_type_name, msmt_values_dict in msmt_type_dict.items():
			try:
				msmt_category_object = sess.query(MeasurementItemCategory).\
					filter(MeasurementItemCategory.category_name == msmt_category_name).one()

				msmt_type_object = sess.query(MeasurementItemType).\
					filter(MeasurementItemType.type_name == msmt_type_name).one()
			except NoResultFound:
				raise
			start_range = msmt_values_dict['measurement'] - msmt_values_dict['tolerance']
			end_range = msmt_values_dict['measurement'] + msmt_values_dict['tolerance']
			pref = UserMeasurementPreference(
				ebay_item_category=ebay_item_category_object,
				measurement_category=msmt_category_object,
				measurement_type=msmt_type_object,
				user_account=user_object,
				range_start_value=start_range,
				range_end_value=end_range
			)
			pref_models.append(pref)

	return pref_models







