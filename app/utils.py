import app.models
from app import db

SUPPORTED_CLOTHING = ['suits', 'sportcoats', 'shirts', 'shoes', 'outerwear', 'pants']

def diff_preference_changes(user_sizes_dict, request_form_dict):
	"""
	Generates and returns a dict which details the diffs between a user's sizes and 
	new information from a preferences form.preferences
	
	diff_preference_changes compares user_sizes_dict, which is understood to be a dict copy
	of the current size preferences for a User. The function takes these values and diffs
	them against the presence or absence of values in request_form_object. 

	Because request_form_object is coming from a view that generates checkboxes, the 'unchecking'
	of a box causes the value to no longer be present. There isn't a way to log that a user
	wishes to 'unsubscribe' from a size pref other than to compare the present 'checked' boxes
	held in request_form_object and what is present in user_sizes_dict. A disparity indicates a 
	change.

	Parameters
	----------
	user_sizes_dict : dict
		A dictionary in the form:
		{
			"Shirting": {
				"Sleeve": {"30.00": True, ... , "38.00": False},
				"Neck": {...}
			},
			"Sportcoat": {
				"Chest": {...},
				...
			},
			...
		}
	request_form_object : dict
		A dictionary in the form:
		{"size-shirt-dress": 30.00, "size-shirt-dress": 30.25}

	Returns
	-------
	dict
		Dictionary in form:
		{"size-shirt-dress": [(30.00, True), (30.25, False)]} 
		
		# Where each tuple represents a disparity. Values that haven't
		# changed are not listed
	"""
	pass

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




