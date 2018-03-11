import app.models
from app import db

SUPPORTED_CLOTHING = ['suits', 'sportcoats', 'shirts', 'shoes', 'outerwear', 'pants']

def cat_size_prefs(category, user_id):
	cat_prefs = {}

	if category in SUPPORTED_CLOTHING:
		if category == 'shirts':
			cat_prefs.casual = db.Session.query(app.models.LinkUserSizeShirtCasual).filter(
				app.models.LinkUserSizeShirtCasual.user_id == user_id)
		return cat_prefs
	else:
		raise BaseException

# range function with floats
def frange(start, stop, jump):
	i = start
	while i < stop:
		yield i
		i += jump

# this should be done as an event after table creation, but i don't know
# how to do that yet
def populate_size_tables():

	shirt_dress_neck_values = []
	for i in frange(14.00, 20.00, .50):
		size = app.models.SizeKeyShirtDressNeck(size=i)
		shirt_dress_neck_values.append(size)

	shirt_dress_sleeve_values = []
	for i in frange(30.00, 38.00, .25):
		size = app.models.SizeKeyShirtDressSleeve(size=i)
		shirt_dress_sleeve_values.append(size)

	shirt_casual_values = []
	shirt_casual_shorts = ["XS", "S", "M", "L", "XL", "XXL"]
	shirt_casual_longs = ["Exta Small", "Small", "Medium", "Large", "Extra Large", "Extra Extra Large"]

	for i in range(len(shirt_casual_shorts)):
		size = app.models.SizeKeyShirtCasual(
			size_short=shirt_casual_shorts[i], size_long=shirt_casual_longs[i])
		shirt_casual_values.append(size)

	print(shirt_casual_values)

	#db.session.add_all(shirt_dress_neck_values)
	#db.session.add_all(shirt_dress_sleeve_values)
	#db.session.add_all(shirt_casual_values)
	#db.session.commit()




