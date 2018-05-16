import app.models
from app import db
from app.dbtouch import get_user_sizes_subscribed, \
	append_list_of_sizes_to_relationship, \
	remove_list_of_sizes_from_relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

SUPPORTED_CLOTHING = ['suits', 'sportcoats', 'shirts', 'shoes', 'outerwear', 'pants']


def int_to_decimal(integer):
	"""
	Takes integer, divides it by 100, and returns a string formatted to preserve 2
	decimal places

	Parameters
	----------
	integer : integer

	Returns
	-------
	String : str
		In format: {:.2f}
	"""

	string = "{:.2f}".format(integer / 100)
	return string


def update_user_sizes(updates_dict, user_object):
	"""
	Controls the addition or removal of sizes from a User in the database.

	Each item in the dictionary is understood to represents a single table. The
	organization is flat, not heirarchical: instead of being organized as
	shirt(sleeve/neck/casual), it is (shirt-sleeve/shirt-neck/shirt-casual).

	Issues a db.flush() if successful.

	Parameters
	----------
	updates_dict : dict
		Dict is expected to be in the form:
			{size-cat-and-specific: {'add': [size_to_add], 'remove': [size_to_remove]},
			nect-size-cat-and-specific: {'add': [...], 'remove': [...]}}

			example: {'shirt-sleeve': {'add': [30.00, 31.00], 'remove': [32.00]}}
	user_object : object
		user_object is assumed to be a User model

	Returns
	-------
	None
	"""

	user_object.all_sizes_in_dict()
	relationships_dict = user_object.sizes
	ud = updates_dict

	for key, change_dicts in ud.items():
		if len(change_dicts['add']) > 0:
			try:
				append_list_of_sizes_to_relationship(
					relationships_dict[key]['relationship'],
					app.models.model_directory_dict[key],
					change_dicts['add'])
			except ValueError:
				raise
		if len(change_dicts['remove']) > 0:
			try:
				remove_list_of_sizes_from_relationship(
					relationships_dict[key]['relationship'],
					app.models.model_directory_dict[key],
					change_dicts['remove'])
			except NoResultFound:
				raise
	try:
		db.session.flush()
	except IntegrityError:
		db.session.rollback()
		raise


def diff_preference_changes(user_sizes_dict, request_form_dict):
	"""
	Generates and returns a dict which details the diffs between a user's sizes and
	new information gathered from a form on a preferences page (request_form_dict).
	
	diff_preference_changes compares user_sizes_dict, understood to be a dict copy
	of the current size preferences for a User before updates, against new information.
	The function takes these values and diffs them against the presence or absence of
	values in request_form_object, which represent changes the user wishes to make.

	Because request_form_object is coming from a view that generates checkboxes,
	the 'unchecking' of a box causes the value to no longer be present.
	There isn't a way (without JS) to log that a user wishes to 'unsubscribe' from
	a size pref other than to compare the present (and now absent) 'checked' boxes
	held in request_form_object and what is present in user_sizes_dict.
	A disparity indicates a change.

	Parameters
	----------
	user_sizes_dict : dict
		A dictionary in the form:
		{
			"shirt-sleeve": [3000, 3100],
			"shirt-neck": [1550, 1600],
			"sportcoat-chest": [40, 41]
		}
	request_form_dict : dict
		A dictionary also in the form:
		{
			"shirt-sleeve": [3100, 3200], # Notice this list has different values
			"shirt-neck": [1500, 1475]
		}

	Returns
	-------
	dict
		- Dictionary in form:
		{
			"shirt-dress-sleeve": {"add": [3000, 3100], "remove": [3200]},
			"pants-length": {"add": [], "remove": [3300]}
		}
		These values represent the set differences between user_sizes_dict and
		request_form_dict. These differences represent CHANGES the user wishes
		to make to the state held in DB.
	"""

	update_dict = {}

	for name, values_list in user_sizes_dict.items():
		# If working properly, user_sizes_dict will have a name for ALL possible
		# size categories, even if the values_list is empty.
		db_set = set(values_list)
		try:
			form_set = set(request_form_dict[name])
		except KeyError:
			form_set = set()

		remove = db_set - form_set
		add = form_set - db_set

		update_dict[name] = {"add": [x for x in add], "remove": [x for x in remove]}

	return update_dict


def get_size_vals_only(db_sizes_table):
	"""
	Takes an instrumented list (of objects which will always have a `size` attribute)
	and returns a list of only the size attributes.

	Parameters
	----------
	db_sizes_table : instrumentedList
		This is most commonly accessed by Model.relationship
		IE: User.sz_shirt_dress_sleeve

	Return
	------
	list
		Form:
		[30.00, 31.00, 32.00]
	"""

	return [size_obj.size for size_obj in db_sizes_table]


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
	while i <= stop:
		yield i
		i += jump


# this should be done as an event after table creation, but i don't know
# how to do that yet
def populate_size_tables():

	shirt_dress_neck_values = []
	for i in frange(14.00, 20.00, .25):
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

	#print(shirt_casual_values)
	#print(shirt_dress_sleeve_values)
	#print(shirt_dress_neck_values)

	db.session.add_all(shirt_dress_neck_values)
	db.session.add_all(shirt_dress_sleeve_values)
	db.session.add_all(shirt_casual_values)
	db.session.commit()


def populate_size_tables2():

	shirt_dress_neck_values = []
	for i in range(1400, 2000, 25):
		size = app.models.SizeKeyShirtDressNeck(size=i)
		shirt_dress_neck_values.append(size)

	shirt_dress_sleeve_values = []
	for i in range(3000, 3800, 25):
		size = app.models.SizeKeyShirtDressSleeve(size=i)
		shirt_dress_sleeve_values.append(size)

	shirt_casual_values = []
	shirt_casual_shorts = ["XS", "S", "M", "L", "XL", "XXL"]
	shirt_casual_longs = ["Exta Small", "Small", "Medium", "Large", "Extra Large", "Extra Extra Large"]

	for i in range(len(shirt_casual_shorts)):
		size = app.models.SizeKeyShirtCasual(
			size_short=shirt_casual_shorts[i], size_long=shirt_casual_longs[i])
		shirt_casual_values.append(size)

	#print(shirt_casual_values)
	#print(shirt_dress_sleeve_values)
	#print(shirt_dress_neck_values)

	db.session.add_all(shirt_dress_neck_values)
	db.session.add_all(shirt_dress_sleeve_values)
	db.session.add_all(shirt_casual_values)
	db.session.commit()
