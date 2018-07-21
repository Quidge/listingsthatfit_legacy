import datetime
from sqlalchemy import or_, and_, between, func, table, column, alias
from app import db
from app.models import Item, ItemMeasurement as ItemMsmt, EbayItemCategory, MeasurementItemType, MeasurementItemCategory


class MeasurementQueryParameter(object):
	"""This is stupid.

	Attributes
	----------
	category_name : str
	type_name : str
	measurement: int
	tolerance : int
	"""

	def __init__(self, category_name, type_name, measurement, tolerance=0):
		try:
			assert type(measurement) == int
		except AssertionError:
			raise TypeError(
				'Measurement must be instantiated with with an int as the measurement \
				value, value given is: <{}>'.format(measurement_value))
		try:
			assert type(tolerance) == int
		except AssertionError:
			raise TypeError(
				'Measurement must be instantiated with with an int as the tolerance \
				value, value given is: <{}>'.format(tolerance))

		self.category_name = category_name
		self.type_name = type_name
		self.measurement = measurement
		self.tolerance = tolerance

	def __repr__(self):
		return '{}, {}: measurement: {}, tolerance: {}'.format(
			self.category_name, self.type_name, self.measurement, self.tolerance)


def matching_in_categories(cat_msmts_dict, with_measurements=False):
	"""Searches the db for items matching an ad hoc dict composed of
	MeasurementItemType.type_name and ItemMeasurement measurement values.
	Does not search for categories. A chest_flat measurement will return
	suits and shirts matching that measurement.

	Parameters
	----------
	m_dict : dict
		In form:
			{
				'chest_flat': {'measurement': 24000, 'tolerance': 500},
				'shoulders': {'measurement': 18500, 'tolerance': 500}
			}

	Returns
	-------
	items : SQLAlchemy query object
		NOTE: This is NOT a results object. Run .all() on the return value
		to execute the query and return results.
	"""

	s = db.session

	and_components = []
	for ebay_category_id, m_dict in cat_msmts_dict.items():
		for name, sub_dict in m_dict.items():
			and_component = and_(
				EbayItemCategory.category_number == ebay_category_id,
				MeasurementItemType.type_name == name,
				between(
					ItemMsmt.measurement_value,
					sub_dict['measurement'] - sub_dict['tolerance'],
					sub_dict['measurement'] + sub_dict['tolerance'])
			)
			and_components.append(and_component)

	ad_hoc_msmts2 = s.query(
		ItemMsmt._ebay_item_id.label('item_id'),
		func.count('*').label('count'),
		EbayItemCategory.category_number.label('category_number')).\
		join(MeasurementItemType).\
		join(Item, Item.id == ItemMsmt._ebay_item_id).\
		join(EbayItemCategory, Item._primary_ebay_category_id == EbayItemCategory.id).\
		filter(or_(*and_components)).\
		group_by(ItemMsmt._ebay_item_id, EbayItemCategory.category_number).\
		subquery()

	or_components = []
	for ebay_category_id, m_dict in cat_msmts_dict.items():
		or_component = and_(
			ad_hoc_msmts2.c.category_number == ebay_category_id,
			ad_hoc_msmts2.c.count == len(cat_msmts_dict[ebay_category_id]))
		or_components.append(or_component)

	items = s.query(Item).\
		join(
			ad_hoc_msmts2,
			and_(
				Item.id == ad_hoc_msmts2.c.item_id,
				or_(*or_components)
			)
		)

	if with_measurements:
		items = s.query(Item.id).\
			join(
				ad_hoc_msmts2,
				and_(
					Item.id == ad_hoc_msmts2.c.item_id,
					or_(*or_components)
				)
			).\
			subquery()
		w_msmts = s.query(Item, ItemMsmt).\
			join(items, items.c.id == Item.id).\
			join(ItemMsmt)
		return w_msmts

	return items


def matching_in_categories_alt(cat_msmts_dict, with_measurements=False):
	"""Searches the db for items matching an ad hoc dict composed of
	MeasurementItemType.type_name and ItemMeasurement measurement values.
	Does not search for categories. A chest_flat measurement will return
	suits and shirts matching that measurement.

	Parameters
	----------
	m_dict : dict
		In form:
			{
				'chest_flat': {'measurement': 24000, 'tolerance': 500},
				'shoulders': {'measurement': 18500, 'tolerance': 500}
			}

	Returns
	-------
	items : SQLAlchemy query object
		NOTE: This is NOT a results object. Run .all() on the return value
		to execute the query and return results.
	"""

	s = db.session

	'''sample_dict = {
		11484: {
			'measurements_list': [
				MQP('sweater', 'chest_flat', 21750, tolerance=1000),
				MQP('sweater', 'sleeve_from_armpit', 22500, tolerance=1000),
				MQP('sweater', 'sleeve', 26500, tolerance=1000),
				MQP('sweater', 'shoulders_raglan', 0),
				MQP('sweater', 'shoulders', 18500, tolerance=1000)],
			'required_count': 3
		}
	}'''

	user_msmt_join_conditions = []
	print(cat_msmts_dict)
	for ebay_category_id, m_dict in cat_msmts_dict.items():
		for mqp in m_dict['measurements_list']:
			print('category: {}'.format(ebay_category_id), mqp)
			# print(mqp.measurement + mqp.tolerance)
			# print(mqp.measurement - mqp.tolerance)
			# print(mqp)
			and_component = and_(
				Item.end_date > datetime.datetime.now(),
				EbayItemCategory.category_number == ebay_category_id,
				MeasurementItemCategory.category_name == mqp.category_name,
				MeasurementItemType.type_name == mqp.type_name,
				between(
					ItemMsmt.measurement_value,
					mqp.measurement - mqp.tolerance,
					mqp.measurement + mqp.tolerance)
			)
			user_msmt_join_conditions.append(and_component)

	'''ad_hoc_msmts2 = s.query(
		ItemMsmt._ebay_item_id.label('item_id'),
		func.count('*').label('count'),
		EbayItemCategory.category_number.label('category_number')).\
		join(ItemMsmt.measurement_category).\
		join(ItemMsmt.measurement_type).\
		join(Item, Item.id == ItemMsmt._ebay_item_id).\
		join(EbayItemCategory, Item._primary_ebay_category_id == EbayItemCategory.id).\
		filter(or_(*user_msmt_join_conditions)).\
		group_by(ItemMsmt._ebay_item_id, EbayItemCategory.category_number).\
		subquery()'''

	counts = s.query(
		ItemMsmt._ebay_item_id.label('item_id'),
		func.count('*').label('count'),
		EbayItemCategory.category_number.label('category_number')).\
		join(MeasurementItemCategory, ItemMsmt._measurement_category_id == MeasurementItemCategory.id).\
		join(MeasurementItemType, ItemMsmt._measurement_type_id == MeasurementItemType.id).\
		join(Item, Item.id == ItemMsmt._ebay_item_id).\
		join(EbayItemCategory, Item._primary_ebay_category_id == EbayItemCategory.id).\
		filter(or_(*user_msmt_join_conditions)).\
		group_by(ItemMsmt._ebay_item_id, EbayItemCategory.category_number).\
		order_by(EbayItemCategory.category_number)

	print(counts.all())

	ad_hoc_msmts2 = counts.subquery()

	'''item_msmt_matches = s.query(Item).\
		join(ItemMsmt).\
		join(MeasurementItemCategory,
			ItemMsmt._measurement_category_id == MeasurementItemCategory.id).\
		join(MeasurementItemType,
			ItemMsmt._measurement_type_id == MeasurementItemType.id).\
		join(EbayItemCategory, Item._primary_ebay_category_id == EbayItemCategory.id).\
		filter(
			or_(*and_components
			)
		)'''

	# print(item_msmt_matches.count())

	# print(item_msmt_matches.compile())

	# print(item_msmt_matches.count())

	or_components = []
	for ebay_category_id, _ in cat_msmts_dict.items():
		or_component = and_(
			ad_hoc_msmts2.c.category_number == ebay_category_id,
			ad_hoc_msmts2.c.count == cat_msmts_dict[ebay_category_id]['required_count'])
		or_components.append(or_component)

	items = s.query(Item).\
		join(
			ad_hoc_msmts2,
			and_(
				Item.id == ad_hoc_msmts2.c.item_id,
				or_(*or_components)
			)
		)

	if with_measurements:
		items = s.query(Item.id).\
			join(
				ad_hoc_msmts2,
				and_(
					Item.id == ad_hoc_msmts2.c.item_id,
					or_(*or_components)
				)
			).\
			subquery()
		w_msmts = s.query(Item, ItemMsmt).\
			join(items, items.c.id == Item.id).\
			join(ItemMsmt)
		return w_msmts

	return items


def find_all_matching(m_dict):
	"""Searches the db for items matching an ad hoc dict composed of
	MeasurementItemType.type_name and ItemMeasurement measurement values.
	Does not search for categories. A chest_flat measurement will return
	suits and shirts matching that measurement.

	Parameters
	----------
	m_dict : dict
		In form:
			{
				'chest_flat': {'measurement': 24000, 'tolerance': 500},
				'shoulders': {'measurement': 18500, 'tolerance': 500}
			}

	Returns
	-------
	items : SQLAlchemy query object
		NOTE: This is NOT a results object. Run .all() on the return value
		to execute the query and return results.
	"""

	s = db.session

	# print('Searching through <{}> items.'.format(Item.query.count()))
	and_components = []
	for name, sub_dict in m_dict.items():
		and_component = and_(
			MeasurementItemType.type_name == name,
			between(
				ItemMsmt.measurement_value,
				sub_dict['measurement'] - sub_dict['tolerance'],
				sub_dict['measurement'] + sub_dict['tolerance'])
		)
		and_components.append(and_component)

	ad_hoc_msmts2 = s.query(
		# ItemMsmt.measurement_value.label('msmt_val'),
		# ItemMsmt.measurement_type.label('msmt_type'),
		ItemMsmt._ebay_item_id.label('item_id'),
		func.count('*').label('count')).\
		join(MeasurementItemType).\
		filter(or_(*and_components)).\
		group_by(ItemMsmt._ebay_item_id).\
		subquery()

	items = s.query(Item).\
		join(ad_hoc_msmts2, Item.id == ad_hoc_msmts2.c.item_id).\
		filter(ad_hoc_msmts2.c.count > 1)

	return items


if __name__ == '__main__':
	'''general_msmts = {
		'chest_flat': {'measurement': 24000, 'tolerance': 500},
		'shoulders': {'measurement': 18500, 'tolerance': 500},
	}
	query = find_all_matching(general_msmts)
	[print(i) for i in query.all()]
	print(query.count())'''

	MQP = MeasurementQueryParameter

	alt_msmts = {
		11484: {
			'measurements_list': [
				MQP('sweater', 'chest_flat', 21750, tolerance=5000),
				MQP('sweater', 'sleeve_from_armpit', 22500, tolerance=5000),
				MQP('sweater', 'sleeve', 26500, tolerance=5000),
				MQP('sweater', 'shoulders_raglan', 0),
				MQP('sweater', 'shoulders', 18500, tolerance=5000)],
			'required_count': 3
		}
	}

	my_shirt_mqp = {
		57991: {
			'measurements_list': [
				MQP('shirt', 'chest_flat', 21000, tolerance=5000),
				MQP('shirt', 'shoulders', 18500, tolerance=5000),
				MQP('shirt', 'sleeve_long', 25000, tolerance=5000)],
			'required_count': 3
		}
	}

	my_shirt_old = {
		57991: {
			'chest_flat': {'measurement': 21000, 'tolerance': 750},
			'shoulders': {'measurement': 18500, 'tolerance': 750},
			'sleeve_long': {'measurement': 25000, 'tolerance': 750}
		}
	}

	general_msmts2 = {
		3002: {
			'chest_flat': {'measurement': 23000, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 500},
			'sleeve': {'measurement': 25500, 'tolerance': 1500},
			'waist_flat': {'measurement': 18000, 'tolerance': 2000},
			'length': {'measurement': 30000, 'tolerance': 500}
		},
		3001: {
			'chest_flat': {'measurement': 24000, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 500},
			'sleeve': {'measurement': 26000, 'tolerance': 2000},
			'waist_flat': {'measurement': 18000, 'tolerance': 2000},
			'length': {'measurement': 30000, 'tolerance': 500}
		},
		57991: {
			'chest_flat': {'measurement': 23000, 'tolerance': 500},
			'shoulders': {'measurement': 18000, 'tolerance': 500},
			'sleeve_long': {'measurement': 26250, 'tolerance': 500}
		},
		57990: {
			'chest_flat': {'measurement': 23000, 'tolerance': 750},
			'shoulders': {'measurement': 18000, 'tolerance': 750},
			'sleeve_long': {'measurement': 26250, 'tolerance': 1000}
		},
		57988: {
			'chest_flat': {'measurement': 24000, 'tolerance': 1000},
			'shoulders': {'measurement': 18500, 'tolerance': 1000},
			'sleeve': {'measurement': 26000, 'tolerance': 2000}
		}
	}

	my_measurements1 = {
		3002: {  # SC
			'chest_flat': {'measurement': 23000, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 500},
			'sleeve': {'measurement': 25000, 'tolerance': 1500},
			'waist_flat': {'measurement': 20500, 'tolerance': 2000},
			'length': {'measurement': 30500, 'tolerance': 750}
		},
		3001: {  # suit
			'chest_flat': {'measurement': 23000, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 500},
			'sleeve': {'measurement': 25000, 'tolerance': 1500},
			'waist_flat': {'measurement': 20500, 'tolerance': 2000},
			'waist_flat': {'measurement': 15500, 'tolerance': 1500},
			'hips_flat': {'measurement': 16000, 'tolerance': 2000},
			'inseam': {'measurement': 31000, 'tolerance': 3000},
			'rise': {'measurement': 10500, 'tolerance': 1000},
		},
		57989: {  # Pants
			'waist_flat': {'measurement': 15500, 'tolerance': 1500},
			'hips_flat': {'measurement': 16000, 'tolerance': 2000},
			'inseam': {'measurement': 31000, 'tolerance': 3000},
			'rise': {'measurement': 10500, 'tolerance': 1000},
		},
		57991: {  # Dress shirt
			'chest_flat': {'measurement': 21500, 'tolerance': 750},
			'shoulders': {'measurement': 18250, 'tolerance': 500},
			'sleeve_long': {'measurement': 25000, 'tolerance': 500}
		},
		57990: {  # Casual shirt
			'chest_flat': {'measurement': 21500, 'tolerance': 1000},
			'shoulders': {'measurement': 18250, 'tolerance': 625},
			'sleeve_long': {'measurement': 25000, 'tolerance': 625}
		},
		57988: {  # Coats and jackets
			'chest_flat': {'measurement': 23500, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 750},
			'sleeve': {'measurement': 25000, 'tolerance': 2250}
		}
	}

	my_measurements_mqp = {
		3002: {  # SC
			'measurements_list': [
				MQP('jacket', 'chest_flat', 21500, 500),
				MQP('jacket', 'shoulders', 18500, 500),
				MQP('jacket', 'sleeve', 25000, 1500),
				MQP('jacket', 'waist_flat', 20500, 2000),
				MQP('jacket', 'length', 30500, 750)],
			'required_count': 5
		},
		3001: {
			'measurements_list': [
				MQP('jacket', 'chest_flat', 21500, 500),
				MQP('jacket', 'shoulders', 18500, 500),
				MQP('jacket', 'sleeve', 25000, 1500),
				MQP('jacket', 'waist_flat', 20500, 2000),
				MQP('jacket', 'length', 30500, 2000),
				MQP('pant', 'waist_flat', 15500, 1500),
				MQP('pant', 'hips_flat', 16000, 2000),
				MQP('pant', 'inseam', 31000, 3000),
				MQP('pant', 'rise', 10500, 1000)
			],
			'required_count': 9
		},
		57989: {  # Pants
			'measurements_list': [
				MQP('pant', 'waist_flat', 15500, 1500),
				MQP('pant', 'hips_flat', 16000, 2000),
				MQP('pant', 'inseam', 31000, 3000),
				MQP('pant', 'rise', 10500, 1000)
			],
			'required_count': 4
		},
		57991: {  # Dress shirts
			'measurements_list': [
				MQP('shirt', 'chest_flat', 21500, 750),
				MQP('shirt', 'shoulders', 18250, 500),
				MQP('shirt', 'sleeve_long', 25000, 500),
				MQP('shirt', 'sleeve_short', 11000, 5000)
			],
			'required_count': 3
		},
		57990: {  # Casual shirts
			'measurements_list': [
				MQP('shirt', 'chest_flat', 21500, 1000),
				MQP('shirt', 'shoulders', 18250, 750),
				MQP('shirt', 'sleeve_long', 25000, 625),
				MQP('shirt', 'sleeve_short', 11000, 5000)
			],
			'required_count': 3
		},
		57988: {  # Coats and jackets
			'measurements_list': [
				MQP('jacket', 'chest_flat', 23500, 500),
				MQP('jacket', 'shoulders', 18500, 750),
				MQP('jacket', 'sleeve', 25000, 3000)
			],
			'required_count': 3
		}
	}


	stitches_mqp = {
		3002: {  # SC
			'measurements_list': [
				MQP('jacket', 'chest_flat', 22000, 500),
				MQP('jacket', 'shoulders', 19000, 500),
				MQP('jacket', 'sleeve', 24250, 1500),
				MQP('jacket', 'waist_flat', 21500, 1500),
				MQP('jacket', 'length', 31000, 750)],
			'required_count': 5
		},
		3001: {
			'measurements_list': [
				MQP('jacket', 'chest_flat', 22000, 500),
				MQP('jacket', 'shoulders', 19000, 500),
				MQP('jacket', 'sleeve', 24250, 1500),
				MQP('jacket', 'waist_flat', 21500, 1500),
				MQP('jacket', 'length', 31000, 750),
				MQP('pant', 'waist_flat', 19500, 1500),
				MQP('pant', 'hips_flat', 12750, 1000),
				MQP('pant', 'inseam', 32000, 3000),
				MQP('pant', 'rise', 11000, 500)
			],
			'required_count': 9
		},
		57989: {  # Pants
			'measurements_list': [
				MQP('pant', 'waist_flat', 19500, 1500),
				MQP('pant', 'hips_flat', 12750, 1000),
				MQP('pant', 'inseam', 32000, 3000),
				MQP('pant', 'rise', 11000, 500)
			],
			'required_count': 4
		},
		57991: {  # Dress shirts
			'measurements_list': [
				MQP('shirt', 'chest_flat', 24250, 250),
				MQP('shirt', 'shoulders', 19750, 500),
				MQP('shirt', 'sleeve_long', 25500, 500),
				MQP('shirt', 'sleeve_short', 11000, 5000)
			],
			'required_count': 3
		},
		57990: {  # Casual shirts
			'measurements_list': [
				MQP('shirt', 'chest_flat', 24250, 250),
				MQP('shirt', 'shoulders', 19750, 500),
				MQP('shirt', 'sleeve_long', 25500, 500),
				MQP('shirt', 'sleeve_short', 11000, 5000)
			],
			'required_count': 3
		},
		57988: {  # Coats and jackets
			'measurements_list': [
				MQP('jacket', 'chest_flat', 22500, 1000),
				MQP('jacket', 'shoulders', 19250, 500),
				MQP('jacket', 'sleeve', 24250, 1500),
			],
			'required_count': 3
		}
	}

	query6 = matching_in_categories_alt(stitches_mqp, with_measurements=True)
	# [print(i.ebay_item_id, i.measurements) for i in query6.all()]
	[print(i) for i in query6.all()]
	print(query6.count())
	# print(query6.count())
	# query2 = matching_in_categories(general_msmts2, with_measurements=True)
	# query3 = matching_in_categories_alt(alt_msmts)
	# [print(i) for i in query3.all()]
	# print(query3.count())
	# query4 = matching_in_categories_alt(my_shirt_mqp, with_measurements=False)
	# query5 = matching_in_categories(my_measurements1, with_measurements=False)
	# [print(i.ebay_title) for i in query5.all()]
	# print(query5.count())
	# print(query5.all())
	# [print(m) for i, m in query2.all()]
	# [print(row) for row in query2.all()]
	# from app.reporter.utils import compile_item_with_measurements as compile
	# items_dict = compile(query2.all())
	'''for item, msmt in query2.all():
		items_dict[item.ebay_item_id] = {'item_details': item, 'measurements': []}
	# print(query2.count())
	for item, msmt in query2.all():
		items_dict[item.ebay_item_id]['measurements'].append(msmt)'''

	# print(len(items_dict))
	# print(items_dict)









