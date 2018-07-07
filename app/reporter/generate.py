from app.reporter import jinja_env


def output_forum_post(list_of_items, metadata=None):
	template = jinja_env.get_template('base_forum_post.txt')
	print(template.render(items=list_of_items, metadata=metadata))


def output_forum_post_w_msmts(results_dict, metadata=None):
	template = jinja_env.get_template('base_forum_post_w_msmts.txt')
	print(template.render(items=results_dict, metadata=metadata))


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
	spoo_msmts = {
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

	}
	q = adhoc_cat(spoo_msmts, with_measurements=True)
	compressed = compress(q.all())
	meta = {
		'total_search_count': Item.query.count(),
		'result_count': len(compressed),
		'measurements_provided': spoo_msmts
	}
	output_forum_post_w_msmts(compressed, metadata=meta)








