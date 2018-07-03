from sqlalchemy import and_, between, func

from app.models import Item, ItemMeasurement as ItemMsmt, EbayItemCategory, User
from app.models import UserMeasurementPreference as UserPref


def find_items_matching_user_measurements(
	user_id,
	db_connection,
	ebay_item_category=None):
	"""Returns a list of Item where the Items associated ItemMeasurements match
	UserMeasurementPreferences for the given user_id parameter.

	Parameters
	----------
	user_id : int
	db_connection : db connection
	ebay_item_category : int

	Returns
	-------
	res : list
		Result list containing Item instances
	"""

	if ebay_item_category is not None:
		raise ValueError('ebay_item_category parameter is not supported at this time.')

	s = db_connection.session

	user_pref_sq = s.query(
		UserPref.id.label('user_measurement_preference_id'),
		UserPref._category_id.label('_category_id'),
		UserPref._type_id.label('_type_id'),
		UserPref._ebay_category_id.label('_ebay_category_id'),
		UserPref.range_start_value.label('range_start_value'),
		UserPref.range_end_value.label('range_end_value')).\
		filter(UserPref._user_account_id == user_id).\
		subquery('user_pref_sq')

	"""
	print('Get only only preferences for user_id={}'.format(user_id))
	print('Query:\n{}'.format(user_pref_sq))
	print('Result count: {}'.format(user_pref_sq.count()))
	print()
	"""

	# Join all Items with ItemMeasurements, and outer join any UserPreferences that
	# match ItemMeasurements
	item_oj_to_up_q = s.query(
		Item.ebay_item_id,
		ItemMsmt.id,
		user_pref_sq.c.user_measurement_preference_id).\
		join(ItemMsmt).\
		join(user_pref_sq, and_(
			user_pref_sq.c._category_id == ItemMsmt._measurement_category_id,
			user_pref_sq.c._type_id == ItemMsmt._measurement_type_id,
			user_pref_sq.c._ebay_category_id == Item._primary_ebay_category_id,
			between(
				ItemMsmt.measurement_value,
				user_pref_sq.c.range_start_value,
				user_pref_sq.c.range_end_value)
			),
		isouter=True)

	"""
	print('Query all Items, join with ItemMeasurements, outer join with user_id={} \
		UserMeasurementPreferences that match ItemMeasurements'.format(user_id))
	print('Query:\n{}'.format(item_oj_to_up_q))
	print('Result count: {}'.format(item_oj_to_up_q.count()))
	print()
	"""

	# Turn item_oj_to_up_q into subquery
	item_oj_to_up_sq = item_oj_to_up_q.subquery('item_oj_to_up_sq')

	pref_msmt_count_q = s.query(
			item_oj_to_up_sq.c.ebay_item_id,
			func.count('*').label('pref_count')).\
		select_from(item_oj_to_up_sq).\
		filter(item_oj_to_up_sq.c.user_measurement_preference_id != None).\
		group_by(item_oj_to_up_sq.c.ebay_item_id)

	"""
	print('Group up on itemID and count number of matching UserPreferenceMeasurements \
		for that itemID. Call this subquery pref_msmt_count_sq.')
	print('Query:\n{}'.format(pref_msmt_count_q))
	print('Result count: {}'.format(pref_msmt_count_q.count()))
	print()
	"""

	# Turn pref_msmt_count_q into subquery
	pref_msmt_count_sq = pref_msmt_count_q.subquery('pref_msmt_count_sq')

	item_w_msmt_q = s.query(Item).\
		join(ItemMsmt, Item.id == ItemMsmt._ebay_item_id)

	"""
	print('Query for all Items joined with their ItemMeasurements')
	print('Query:\n{}'.format(item_w_msmt_q))
	print('Result count: {}'.format(item_w_msmt_q.count()))
	print()
	"""

	# Turn item_w_msmt_q into subquery
	item_w_msmt_sq = item_w_msmt_q.subquery('item_w_msmt_sq')

	item_msmt_count_q = s.query(
			item_w_msmt_sq.c.ebay_item_id, func.count('*').label('item_count')).\
		select_from(item_w_msmt_sq).\
		group_by(item_w_msmt_sq.c.ebay_item_id)

	"""
	print('Group up on itemID and count number of matching ItemMeasurement \
		for that itemID. Call this subquery item_msmt_count_sq.')
	print('Query:\n{}'.format(item_msmt_count_q))
	print('Result count: {}'.format(item_w_msmt_q.count()))
	print()
	"""

	# Turn item_msmt_count_q into subquery
	item_msmt_count_sq = item_msmt_count_q.subquery('item_msmt_count_sq')

	r = s.query(Item).\
		join(pref_msmt_count_sq,
			pref_msmt_count_sq.c.ebay_item_id == Item.ebay_item_id).\
		join(item_msmt_count_sq,
			item_msmt_count_sq.c.ebay_item_id == pref_msmt_count_sq.c.ebay_item_id).\
		filter(
			pref_msmt_count_sq.c.pref_count == item_msmt_count_sq.c.item_count)

	"""
	print('Final query. Query all Items, join item_msmt_count_sq, join \
		pref_msmt_count_sq, and only return Items where there are ultimately matching \
		number of appropriate ItemMeasurements and appropriate \
		UserMeasurementPreferences for that item.')
	print('Query:\n{}'.format(r))
	print('Result count: {}'.format(r.count()))
	print()
	"""

	"""
	For what it's worth, this pure SQL query does almost exactly the same thing.
	(Thank you Sheila Leverson!) It doesn't specifiy UserPreferenceMeasurements
	that match a specific user_id.

	select
	pref_msmt.ebay_item_id, pref_msmt.count pref_count, item_msmt.count item_count
	from
	(select ebay_item_id, count(*)
	from
	(select
	    ei.ebay_item_id, im.item_measurement_id, ump.user_measurement_preference_id
	from
	    ebay_items ei
	join
	    item_measurement as im
	on
	    ei.id = im.ebay_items_id
	left outer join
	    user_measurement_preference ump
	on
	    ump.measurement_item_category_id = im.measurement_item_category_id
	and
	    ump.measurement_item_type_id = im.measurement_item_type_id
	and
	    ump.ebay_item_category_id = ei.primary_ebay_item_category_id
	and
	    im.item_measurement_value
	between
	    ump.measurement_range_start_inch_factor and ump.measurement_range_end_inch_factor
	) _subquery
	where
	user_measurement_preference_id is not null
	group by
	ebay_item_id) pref_msmt
	join
	(select ebay_item_id, count(*)
	from (
	select
	ei.*
	from
	    ebay_items ei
	join
	item_measurement im
	on
	ei.id = im.ebay_items_id
	) _subquery2
	group by
	ebay_item_id) item_msmt
	on
	pref_msmt.ebay_item_id = item_msmt.ebay_item_id
	where
	pref_msmt.count = item_msmt.count
	"""

	return r.all()

if __name__ == '__main__':
	from app import db
	res = find_items_matching_user_measurements(
		2, db)
	# [print(i.ebay_item_id, m) for i, m in res]
	'''for item in res:
		print(item.ebay_item_id)
		for m in item.measurements:
			print(m)'''
	[print(i) for i in res]
	print('result len:', len(res))
	print(type(res))






