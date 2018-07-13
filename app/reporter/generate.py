from sqlalchemy.orm.exc import NoResultFound

from app.reporter import reporter_jinja_env as jinja_env
from app.models import Item


def output_forum_post(list_of_items, metadata=None):
	template = jinja_env.get_template('base_forum_post.txt')
	print(template.render(items=list_of_items, metadata=metadata))


def single_item_measurements_report(ebay_item_id):
	try:
		i = Item.query.filter(Item.ebay_item_id == ebay_item_id).one()
	except NoResultFound:
		raise NoResultFound('Could not find an Item instance with ebay ID <{}> in the database.'.format(
			ebay_item_id))
	template = jinja_env.get_template('single_item_forum_post.txt')
	return template.render(item=i, measurements=i.measurements)


def generate_forum_post_w_msmts(list_of_items, metadata=None):
	"""Takes list of rows with (<Item>, <ItemMeasurement>) instances, compresses it to
	a dict of {item : {various: msmt, various2: msmt}}, and renders as text appropriate
	for a Styleforum post.

	Parameters
	----------
	list_of_items : list
		list of tuples in form (and order): (<Item instance>, <ItemMeasurement instance>)
	metadata : dict
		in form {
			'total_search_count': Item.query.count(),
			'result_count': len(compressed),
			'measurements_provided': measurement dict
		}

	Returns
	-------
	rendered template

	"""
	items_dict = compress(list_of_items)
	template = jinja_env.get_template('base_forum_post_w_msmts.txt')
	return template.render(items=items_dict, metadata=metadata)


if __name__ == '__main__':
	from app.instance.query.matching_ad_hoc import find_all_matching as adhoc
	from app.instance.query.matching_ad_hoc import matching_in_categories as adhoc_cat
	from app.reporter.utils import compile_item_with_measurements as compress
	from app.models import Item

	'''wes_msmts = {
		'chest_flat': {'measurement': 19000, 'tolerance': 2000},
		'shoulders': {'measurement': 21000, 'tolerance': 1000},
	}
	q = adhoc(wes_msmts)
	meta = {
		'total_search_count': Item.query.count(),
		'result_count': q.count(),
		'measurements_provided': wes_msmts
	}
	# print('Results: <{}>'.format(q.count()))
	output_forum_post(q.all(), metadata=meta)'''
	'''spoo_msmts = {
		3002: {
			'chest_flat': {'measurement': 22000, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 500},
			'sleeve': {'measurement': 26000, 'tolerance': 2000},
			'waist_flat': {'measurement': 18000, 'tolerance': 2000},
			'length': {'measurement': 30000, 'tolerance': 500}
		},
		3001: {
			'chest_flat': {'measurement': 22000, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 500},
			'sleeve': {'measurement': 26000, 'tolerance': 2000},
			'waist_flat': {'measurement': 18000, 'tolerance': 2000},
			'length': {'measurement': 30000, 'tolerance': 500}
		},
		57991: {
			'chest_flat': {'measurement': 21500, 'tolerance': 500},
			'shoulders': {'measurement': 18000, 'tolerance': 500},
			'sleeve': {'measurement': 26250, 'tolerance': 500}
		},
		57990: {
			'chest_flat': {'measurement': 21500, 'tolerance': 750},
			'shoulders': {'measurement': 18000, 'tolerance': 750},
			'sleeve': {'measurement': 26250, 'tolerance': 1000}
		},
		57988: {
			'chest_flat': {'measurement': 22000, 'tolerance': 1000},
			'shoulders': {'measurement': 18500, 'tolerance': 1000},
			'sleeve': {'measurement': 26000, 'tolerance': 2000}
		}
	}'''

	my_measurements20180710 = {
		3002: {  # SC
			'chest_flat': {'measurement': 21750, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 500},
			'sleeve': {'measurement': 25000, 'tolerance': 1500},
			'waist_flat': {'measurement': 20500, 'tolerance': 2000},
			'length': {'measurement': 30500, 'tolerance': 750}
		},
		3001: {  # suit
			'chest_flat': {'measurement': 21750, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 500},
			'sleeve': {'measurement': 25000, 'tolerance': 1500},
			'waist_flat': {'measurement': 20500, 'tolerance': 2000},
			'waist_flat': {'measurement': 15500, 'tolerance': 1500},
			'hips_flat': {'measurement': 16000, 'tolerance': 2000},
			'inseam': {'measurement': 31000, 'tolerance': 3000},
			'rise': {'measurement': 10500, 'tolerance': 1000},
		},
		57989: {  # Pants
			'waist_flat': {'measurement': 15500, 'tolerance': 1500},
			'hips_flat': {'measurement': 16000, 'tolerance': 2000},
			'inseam': {'measurement': 31000, 'tolerance': 3000},
			'rise': {'measurement': 10500, 'tolerance': 1000},
		},
		57991: {  # Dress shirt
			'chest_flat': {'measurement': 21500, 'tolerance': 750},
			'shoulders': {'measurement': 18250, 'tolerance': 500},
			'sleeve_long': {'measurement': 25000, 'tolerance': 500}
		},
		57990: {  # Casual shirt
			'chest_flat': {'measurement': 21500, 'tolerance': 1000},
			'shoulders': {'measurement': 18250, 'tolerance': 625},
			'sleeve_long': {'measurement': 25000, 'tolerance': 625}
		},
		57988: {  # Coats and jackets
			'chest_flat': {'measurement': 21750, 'tolerance': 500},
			'shoulders': {'measurement': 18500, 'tolerance': 750},
			'sleeve': {'measurement': 25000, 'tolerance': 2250}
		}
	}

	import copy
	my_measurements20180710_looser = copy.deepcopy(my_measurements20180710)

	# print(my_measurements20180710_looser, id(my_measurements20180710_looser))
	# print(my_measurements20180710, id(my_measurements20180710))

	for _, m_dict in my_measurements20180710_looser.items():
		for m_type, msmt_values in m_dict.items():
			msmt_values['tolerance'] = int(msmt_values['tolerance'] * 1.4)

	# print(my_measurements20180710_looser, id(my_measurements20180710_looser))
	# print(my_measurements20180710, id(my_measurements20180710))

	q = adhoc_cat(my_measurements20180710, with_measurements=True)
	q_looser = adhoc_cat(my_measurements20180710_looser, with_measurements=True)
	print(q.count(), q_looser.count())

	results = q.all()

	meta = {
		'total_search_count': Item.query.count(),
		'result_count': len(compress(results)),
		'measurements_provided': my_measurements20180710
	}
	report = generate_forum_post_w_msmts(results, metadata=meta)
	print(report)








