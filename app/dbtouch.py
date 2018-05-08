from app import app, db
from app.models import User, SizeKeyShirtDressSleeve, SizeKeyShirtDressNeck, SizeKeyShirtCasual
from app.models import LinkUserSizeShirtDressSleeve, LinkUserSizeShirtCasual, LinkUserSizeShirtDressNeck
# from app.utils import get_size_vals_only
from sqlalchemy import select


def update_user_sizes(updates_dict, user_object):
	"""
	Controls the addition or removal of sizes from a User in the database.

	Each item in the dictionary is understood to represents a single table. The hierarchy
	is flat: not organized by shirt: sleeve/neck/casual, but
	shirt-sleeve/shirt-neck/shirt-casual.

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
	'''
	ud = updates_dict
	if len(ud['shirt-sleeve']['add']) != 0 or len(ud['shirt-sleeve']['remove']) != 0:
		from app.models import SizeKeyShirtDressSleeve
		if len(ud['shirt-sleeve']['add']) != 0:
			append_list_of_sizes_to_relationship(
				user_object.sz_shirt_dress_sleeve,
				SizeKeyShirtDressSleeve,
				ud['shirt-sleeve']['add']
			)
		if len(ud['shirt-sleeve']['remove']) != 0:
			remove_list_of_sizes_from_relationship(
				user_object.sz_shirt_dress_sleeve,
				SizeKeyShirtDressSleeve,
				ud['shirt-sleeve']['remove']
			)
	'''
	pass


def append_list_of_sizes_to_relationship(relationship, model, values_list, match_attr):
	"""
	Associates a list of primitive values contained in values_list with a model and
	appends each of those size models to the provided relationship.

	Issues a rollback if any exceptions are raised.

	Parameters
	----------
	relationship : SQLAlchemy relationship()
		Say model was SizeKeyShirtDressSleeve - relationship would be User.sz_shirt_dress_sleeve
	model : SQLAlchemy model
		Model will correspond to the model type for the relationship
	values_list : list
		For example, a list of values for SizeShirtDressSleeve [3000, 3150, 3100]
	match_attr : the attribute name on the model that each value in values_list
					will be matched against

	Returns
	-------
	None
	"""
	try:
		for value in values_list:
			size_obj = db.session.query(model).filter(model[match_attr] == value).first()
			relationship.append(size_obj)
	except BaseException:
		db.session.rollback()
		raise


def remove_list_of_sizes_from_relationship(relationship, model, values_list, match_attr):
	"""
	Associates a list of primitive values contained in values_list with a model and
	removes each of those size models from the provided relationship (expected to be
	a User size relationship).

	Issues a rollback if any exceptions are raised.

	Parameters
	----------
	relationship : SQLAlchemy relationship()
		Say model was SizeKeyShirtDressSleeve - relationship would be User.sz_shirt_dress_sleeve
	model : SQLAlchemy model
		Model will correspond to the model type for the relationship
	values_list : list
		For example, a list of values for SizeShirtDressSleeve [3000, 3150, 3100]
	match_attr : the attribute name on the model that each value in values_list
					will be matched against

	Returns
	-------
	None
	"""
	try:
		for value in values_list:
			size_obj = db.session.query(model).filter(model[match_attr] == value).first()
			relationship.remove(size_obj)
	except BaseException:
		db.session.rollback()
		raise


def get_user_sizes_subscribed(user_object):
	"""
	Returns a dict of subscribed sizes in a list. Each dict key corresponds to a
	different size table.

	Parameters
	----------
	user_object : object
		user_object is assumed to be a User model

	Returns
	-------
	dict
		Form:

		{
			"shirt-dress-sleeve": [30.00, 30.50, 31.00],
			"shirt-dress-neck": [16.00, 16.25, 16.50],
			"sportcoat-chest": ['40', '41']
			"sportcoat-length": ['R', 'L']
		}
	"""
	user_sizes_subscribed = {
		"shirt-sleeve": [size_obj.size for size_obj in user_object.sz_shirt_dress_sleeve],
		"shirt-neck": [size_obj.size for size_obj in user_object.sz_shirt_dress_neck],
		"shirt-casual": [size_obj.size for size_obj in user_object.sz_shirt_casual]
	}

	return user_sizes_subscribed


def get_user_sizes_join_with_all_possible(user_object):
	"""
	Returns a dictionary of both user_object associated sizes as well as all other
	possible category sizes through lists of two value tuples: (size_value, boolean).

	This dictionary is composed by grabbing the sizes associated with the user, and
	outerjoining them with all possible sizes for that category. The result is a
	hierarchical dictionary where the values are held in a list of two value tuple
	pairs. Each hierarchical level has a "cat_key" attribute which diffrentiates it from
	sibling levels.

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
		embeded in HTML values, which can the be re-parsed.

	"""

	# -- Shirt Dress Sleeves
	usr_lt_shirt_sleeve = (
		select([LinkUserSizeShirtDressSleeve])
		.where(LinkUserSizeShirtDressSleeve.c.user_id == user_object.id)
		.alias())

	shirt_sleeve_sizes = (
		db.session
		.query(SizeKeyShirtDressSleeve.size, usr_lt_shirt_sleeve.c.size_id != None)
		.outerjoin(usr_lt_shirt_sleeve, usr_lt_shirt_sleeve.c.size_id == SizeKeyShirtDressSleeve.id)
		.order_by(SizeKeyShirtDressSleeve.size.asc())
		.all())

	# -- Shirt Dress Neck
	usr_lt_shirt_neck = (
		select([LinkUserSizeShirtDressNeck])
		.where(LinkUserSizeShirtDressNeck.c.user_id == user_object.id)
		.alias())

	shirt_neck_sizes = (
		db.session
		.query(SizeKeyShirtDressNeck.size, usr_lt_shirt_neck.c.size_id != None)
		.outerjoin(usr_lt_shirt_neck, usr_lt_shirt_neck.c.size_id == SizeKeyShirtDressNeck.id)
		.order_by(SizeKeyShirtDressNeck.size.asc())
		.all())

	# -- Shirt Casual
	usr_lt_shirt_casual = (
		select([LinkUserSizeShirtCasual])
		.where(LinkUserSizeShirtCasual.c.user_id == user_object.id)
		.alias())

	shirt_casual_sizes = (
		db.session
		.query(SizeKeyShirtCasual.size_short, usr_lt_shirt_casual.c.size_id != None)
		.outerjoin(usr_lt_shirt_casual, usr_lt_shirt_casual.c.size_id == SizeKeyShirtCasual.id)
		.order_by(SizeKeyShirtCasual.size_short.asc())
		.all())

	user_sizes = {
		"Shirting": {
			"Sleeve": {"values": shirt_sleeve_sizes, "cat_key": "sleeve"},
			"Neck": {"values": shirt_neck_sizes, "cat_key": "neck"},
			"Casual": {"values": shirt_casual_sizes, "cat_key": "casual"},
			"cat_key": "shirt"
		}
	}

	return user_sizes




