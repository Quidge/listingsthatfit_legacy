from app import app, db

def update_user_sizes(updates_dict, user_object):
	"""
	Controls the addition or removal of sizes from a User in the database.

	Parameters
	----------
	updates_dict : dict
		Dict is expected to be in the form:
			{size_cat: {size_specific: [list of tuples (size_val, true/false)]}}

			example: {'shirt-dress': {'sleeve': [(30.00, True), (31.25, False)]}}
	user_object : object
		user_object is assumed to be a User model

	Returns
	-------
	None
	"""
	pass

def get_user_sizes(user_object):
	"""
	Returns size preferences for user_object.

	Composes all susbscribed sizes for a User, and OUTERJOINs that information with all
	possible sizes for those specific size categories.

	For example, if a user is subscribed to Dress Shirt Sleeve Sizes 30.00 and 31.00,
	the return dict object will have {"30.00":True, "30.25":False, ..., "31.00": True}

	Parameters
	----------
	user_object : object
		user_object is assumed to be a User model

	Returns
	-------
	dict
		Returned dictionary will be a dictionary that composes all sizes a user is
		susbscribed to (True), and all other possible values for that size category
		specific (False)

	"""
	pass