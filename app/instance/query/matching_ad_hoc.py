from sqlalchemy import or_, and_, between, func
from app import db
from app.models import Item, ItemMeasurement as ItemMsmt, EbayItemCategory, MeasurementItemType

'''general_msmts = {
	'chest_flat': {'measurement': 24000, 'tolerance': 500},
	'shoulders': {'measurement': 18500, 'tolerance': 500},
}'''


def matching_in_categories(m_dict):
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
	general_msmts = {
		'chest_flat': {'measurement': 24000, 'tolerance': 500},
		'shoulders': {'measurement': 18500, 'tolerance': 500},
	}
	query = find_all_matching(general_msmts)
	[print(i) for i in query.all()]
	print(query.count())









