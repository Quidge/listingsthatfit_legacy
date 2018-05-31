from importlib import import_module


def parse_html_for_measurements(
	item_html_description,
	clothing_category_id,
	seller_id_num):
	"""Takes html_description and seller_id number and returns a dictionary object of
	measurements.

	Parameters
	----------
	item_html_description : str
	category_id : int
	seller_id_num : int

	Returns
	-------
	item_sizes : dict
		In form:
			{
				"chest": 23000,
				"shoulders": 19375,
				... ,
				etc
			}
	"""
	try:
		module_name = 'seller_id_{}'.format(seller_id_num)
		measurements_parser = import_module('app.template_parsing.seller_patterns.{}'.format(module_name))
	except ImportError:
		raise

	if clothing_category_id == 3002:
		return measurements_parser.get_sportcoat_measurements(item_html_description)
	# elif clothing_category_id == other numbers
		# return measurements_parser.other_item_parsers
	else:
		raise AttributeError(
			'Unable to parse items in category <{}>'.format(clothing_category_id))

	return None

