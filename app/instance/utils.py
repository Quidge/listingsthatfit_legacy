import logging
from sqlalchemy import or_, and_, between, func, table, column, alias
from app.models import (
	Item, ItemMeasurement as ItemMsmt, EbayItemCategory, MeasurementItemType,
	MeasurementItemCategory, ClothingCategory)
from app.instance.query.matching_ad_hoc import MeasurementQueryParameter as MQP

logger = logging.getLogger(__name__)


def recurse_construction_schema(tier, m_dict, clothing_category_name):
	"""'construction_tier': ('and', [
				('and', ('sweater', 'chest_flat')),
				('or', [
					('and', [('and', ('sweater', 'shoulders')), ('and', ('sweater', 'sleeve'))]),
					('and', [('and', ('sweater', 'shoulders_raglan')), ('and', ('sweater', 'sleeve_from_armpit'))])
				])
			])"""

	content = tier[1]

	if tier[0] == 'and':
		operator = and_
	elif tier[0] == 'or':
		operator = or_
	else:
		raise ValueError('Improper format. First item must be either "and" or "or".')


	# if instruction != 'and' and instruction != 'or':
		# raise ValueError('Improper format. First item must be either "and" or "or".')
	# elif instruction == 'and':
	# 	clause = and_()

	if type(content) is list:
		# This won't work yet. None of the other returns return lists.
		return operator(*recurse_construction_schema(content, m_dict, clothing_category_name))
	else:
		try:
			mqp = m_dict[content]
		except KeyError:
			raise('Measurements dict does not contain <{}>'.format(content))

		# if instruction == 'and':
			logger.debug((
				'Reached an instruction and simple tuple content. '
				'Attempting to construct clause.'))
			clause = operator(
				ClothingCategory.clothing_category_name == clothing_category_name,
				MeasurementItemCategory.category_name == mqp.category_name,
				MeasurementItemType.type_name == mqp.type_name,
				between(
					ItemMsmt.measurement_value,
					mqp.measurement - mqp.tolerance,
					mqp.measurement + mqp.tolerance))
			logger.debug('Constructed clause')
			return clause






def measurement_block_query_builder(clothing_cat_dict):
	"""Expects something like this:
	{
		'sweater': {  # Sweaters
			'measurements_list': [
				MQP('sweater', 'chest_flat', 24250, 250),
				MQP('sweater', 'shoulders', 19625, 500),
				MQP('sweater', 'shoulders_raglan', 0, 0),
				MQP('sweater', 'sleeve', 26000, 1500),
				MQP('sweater', 'sleeve_from_armpit', 19250, 2000)
			],
			'required_count': 3,
			'construction_schema': ('and', [
				('sweater', 'chest_flat'),
				('or', [
					('and', [('sweater', 'shoulders'), ('sweater', 'sleeve')]),
					('and', [('sweater', 'shoulders_raglan'), ('sweater', 'sleeve_from_armpit')])
				])
			])
		}
	}
	"""
	if len(clothing_cat_dict.keys()) > 1:
		raise ValueError(
			'Expected there to be only one item in the dict passed. Found more than one.')

	clothing_cat_name = list(clothing_cat_dict.keys())[0]
	logger.debug('The clothing category is <{}>'.format(clothing_cat_name))

	clause = None

	m_list = clothing_cat_dict[clothing_cat_name]['measurements_list']

	if clothing_cat_dict[clothing_cat_name]['construction_schema'] is None:
		logger.debug('Constructing clause without using a construction schema')

		ands = []

		for mqp in m_list:
			logger.debug('Turning <{}> into a sqlalchemy statement'.format(mqp))
			and_component = and_(
				ClothingCategory.clothing_category_name == clothing_cat_name,
				MeasurementItemCategory.category_name == mqp.category_name,
				MeasurementItemType.type_name == mqp.type_name,
				between(
					ItemMsmt.measurement_value,
					mqp.measurement - mqp.tolerance,
					mqp.measurement + mqp.tolerance))
			logger.debug('Finished turning a mqp into a sqlalchemy clause. Result clause: {}'.format(and_component))
			ands.append(and_component)
		clause = and_(*ands)
		logger.debug('Finished looping through measurements list. Returning clause.')

		return clause

	else:
		schema = clothing_cat_dict[clothing_cat_name]['construction_schema']
		logger.debug((
			'Constructing clause using the provided construction schema. '
			'construction_schema={}').format(schema))

		logger.debug('Building dictionary from mqp list.')

		mqp_dict = {}
		for mqp in m_list:
			# This uses the mqp to build a tuple that can be used as the key for itself as a value
			mqp_dict[(mqp.category_name, mqp.type_name)] = mqp

		# Okay, here goes.






	"""user_msmt_join_conditions = []
	# print(cat_msmts_dict)
	for clothing_category_name, m_dict in cat_msmts_dict.items():
		for mqp in m_dict['measurements_list']:
			# print('category: {}'.format(ebay_category_id), mqp)
			# print(mqp.measurement + mqp.tolerance)
			# print(mqp.measurement - mqp.tolerance)
			# print(mqp)
			and_component = and_(
				Item.end_date > datetime.datetime.now() + datetime.timedelta(days=days_out),
				ClothingCategory.clothing_category_name == clothing_category_name,
				MeasurementItemCategory.category_name == mqp.category_name,
				MeasurementItemType.type_name == mqp.type_name,
				between(
					ItemMsmt.measurement_value,
					mqp.measurement - mqp.tolerance,
					mqp.measurement + mqp.tolerance)
			)
			user_msmt_join_conditions.append(and_component)"""
