from app.reporter import jinja_env


def output_forum_post(list_of_items, metadata=None):
	template = jinja_env.get_template('base_forum_post.txt')
	print(template.render(items=list_of_items, metadata=metadata))


if __name__ == '__main__':
	from app.instance.query.matching_ad_hoc import find_all_matching as adhoc
	from app.models import Item

	wes_msmts = {
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
	output_forum_post(q.all(), metadata=meta)
