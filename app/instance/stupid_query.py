from sqlalchemy import and_
from app.models import Item, MeasurementType as Type, ItemMeasurementAssociation as Assoc
from app import db


def search_for_matching_measurements(seller, clothing_category_list, category, attribute, msmt, tolerance):
	s = db.session
	msmt_range = [msmt - tolerance, msmt + tolerance]
	print('Search results for clothing categories <{}> with a <{}> measurement from <{}> to <{}>:'.format(
		clothing_category_list, attribute, min(msmt_range), max(msmt_range)))
	print('----------')

	res = s.query(Assoc, Item, Type).\
		filter(Item.ebay_primary_category.in_(clothing_category_list)).\
		filter(Assoc.fk_measurement_id == Type.id).\
		filter(Assoc.fk_ebay_items_id == Item.id).\
		filter(Type.attribute == attribute).\
		filter(Type.clothing_category == category).\
		filter(Assoc.measurement_value >= min(msmt_range)).\
		filter(Assoc.measurement_value <= max(msmt_range)).\
		all()
	return res


if __name__ == '__main__':
	results = search_for_matching_measurements('baearic1', [3001, 3002], 'sportcoat', 'chest', 22000, 1000)
	'''for t, a in results:
		print(a.item.ebay_item_id, ' | ', a.item.ebay_title)
		print(t.clothing_category, t.attribute, a.measurement_value)'''
	[print(
		i.ebay_item_id, i.ebay_title,
		'|', t.attribute, a.measurement_value) for a, i, t in results]
