from sqlalchemy import and_
from app.models import Item, MeasurementType as Type, ItemMeasurementAssociation as Assoc
from app import db


measurements_dict = {}
# measurements_dict = 


def search_for_matching_measurements(seller, clothing_category_list, category, attribute, msmt, tolerance):
	s = db.session
	msmt_range = [msmt - tolerance, msmt + tolerance]
	print('Search results for clothing categories <{}> with a <{}> measurement from <{}> to <{}>:'.format(
		clothing_category_list, attribute, min(msmt_range), max(msmt_range)))
	print('----------')

	'''res = s.query(Assoc, Item, Type).filter(
		Item.ebay_primary_category.in_(clothing_category_list),
		Assoc.fk_measurement_id == Type.id,
		Assoc.fk_ebay_items_id == Item.id,
		Type.attribute == attribute,
		Type.clothing_category == category,
		Assoc.measurement_value >= min(msmt_range),
		Assoc.measurement_value <= max(msmt_range)).\
		all()'''
	res = s.query(Assoc, Item, Type).filter(
		Item.ebay_primary_category.in_(clothing_category_list),
		Assoc.fk_measurement_id == Type.id,
		Assoc.fk_ebay_items_id == Item.id,
		Type.attribute == attribute,
		Type.clothing_category == category,
		Assoc.measurement_value >= min(msmt_range),
		Assoc.measurement_value <= max(msmt_range))

	return res


if __name__ == '__main__':
	results = search_for_matching_measurements('baearic1', [3002], 'sportcoat', 'chest', 22000, 1000)
	'''for t, a in results:
		print(a.item.ebay_item_id, ' | ', a.item.ebay_title)
		print(t.clothing_category, t.attribute, a.measurement_value)'''
	'''[print(
		i.ebay_item_id, i.ebay_title,
		'|', t.attribute, a.measurement_value) for a, i, t in results]'''
	print(results)
