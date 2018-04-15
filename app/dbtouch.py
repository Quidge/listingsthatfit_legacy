from app import app, db
from app.models import User, SizeKeyShirtDressSleeve, LinkUserSizeShirtDressSleeve
from sqlalchemy import select


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
		Form:

		{
			"Shirting": {
				"Sleeve": {"values": [list of tuples], "cat_key": "dress_sleeve"},
				...,
				"cat_key": "shirt"
			}
		}

		Returned dict will be a category based heirarchy. Each tier will have a category
		key ("cat_key"). The actual sizes, "values", will be a list of tuples in
		(value, boolean). In this way all possible sizes in that category and sub
		category will be listed, with True/False values listing whether a user is
		subscribed to that size or not.

		Further, at each tier is a sibling attribute "cat_key". These keys can be iteratively
		embeded in HTML values, which can the be reparsed.
		Returned dictionary will be a dictionary that composes all sizes a user is
		susbscribed to (True), and all other possible values for that size category
		specific (False). These values will be held as tuples in a list. In addition,
		a sibling elemnt to that list of tuples will be a category key string
		EX "shirt-dress-sleeve".

	"""

	user_link_table = (
		select([LinkUserSizeShirtDressSleeve])
		.where(LinkUserSizeShirtDressSleeve.c.user_id == user_object.id)
		.alias())

	shirt_sleeve_sizes = (
		db.session
		.query(SizeKeyShirtDressSleeve.size, user_link_table.c.size_id != None)
		.outerjoin(user_link_table, user_link_table.c.size_id == SizeKeyShirtDressSleeve.id)
		.order_by(SizeKeyShirtDressSleeve.size.asc())
		.all())

	user_sizes = {
		"Shirting": {
			"Sleeve": {"values": shirt_sleeve_sizes, "cat_key": "dress-sleeve"},
			"cat_key": "shirt"
			# "necks": user_object.sz_shirt_dress_neck,
			# "casuals": user_object.sz_shirt_casual
		}
	}

	return user_sizes




