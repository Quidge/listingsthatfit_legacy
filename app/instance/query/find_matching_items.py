from app.models import Item, ItemMeasurementAssociation as Assoc
from app.models import UserMeasurementPreference as Pref

def find_items_matching_user_measurements(
	list_of_user_measurement_preferences,
	db_connection,
	specific_category=None):
	"""Returns a list of Item instances"""

	s = db_connection.session

	results = []

	# I think this involves .any()
	# https://stackoverflow.com/questions/6474989/sqlalchemy-filter-by-membership-in-at-least-one-many-to-many-related-table
	# http://docs.sqlalchemy.org/en/latest/orm/internals.html?highlight=any#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any

	'''res = s.query(Item).filter(
		Item.measurements.\
		any(Assoc.measurement_value >= 22000),
		Item.measurements.\
		any(Assoc.measurement_value <= 2400)).all()'''

	suits_q = s.query(Assoc).join(Pref)

	print(suits_q)

	return suits_q.all()

if __name__ == '__main__':
	from app import db
	res = find_items_matching_user_measurements(
		None, db)
	[print(i.measurements) for i in res]