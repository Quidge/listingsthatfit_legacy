from sqlalchemy import or_, and_, between, func, table, column, alias
from app import db
from app.models import Item, ItemMeasurement as ItemMsmt, EbayItemCategory, MeasurementItemType

"""general_msmts2 = {
	3002: {
		'chest_flat': {'measurement': 24000, 'tolerance': 500},
		'shoulders': {'measurement': 18500, 'tolerance': 500},
	}
}"""


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
		# ItemMsmt.measurement_value.label('msmt_val'),
		# ItemMsmt.measurement_type.label('msmt_type'),
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

	general_msmts2 = {
		3002: {
			'chest_flat': {'measurement': 24000, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 500},
			'sleeve': {'measurement': 26000, 'tolerance': 2000},
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
			'sleeve': {'measurement': 26250, 'tolerance': 500}
		},
		57990: {
			'chest_flat': {'measurement': 23000, 'tolerance': 750},
			'shoulders': {'measurement': 18000, 'tolerance': 750},
			'sleeve': {'measurement': 26250, 'tolerance': 1000}
		},
		57988: {
			'chest_flat': {'measurement': 24000, 'tolerance': 1000},
			'shoulders': {'measurement': 18500, 'tolerance': 1000},
			'sleeve': {'measurement': 26000, 'tolerance': 2000}
		}

	}
	query2 = matching_in_categories(general_msmts2, with_measurements=True)
	# [print(m) for i, m in query2.all()]
	# [print(row) for row in query2.all()]
	from app.reporter.utils import compile_item_with_measurements as compile
	items_dict = compile(query2.all())
	'''for item, msmt in query2.all():
		items_dict[item.ebay_item_id] = {'item_details': item, 'measurements': []}
	# print(query2.count())
	for item, msmt in query2.all():
		items_dict[item.ebay_item_id]['measurements'].append(msmt)'''

	print(len(items_dict))
	print(items_dict)









