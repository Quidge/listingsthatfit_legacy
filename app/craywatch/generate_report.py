from craywatch import jinja_env, finding_connection as f_api
from craywatch.core.pull_items import return_executed_call_for_category, depaginate_item_search_results

category_ids_and_price_cutoff = {
	'sportcoat': {'categoryId': 3002, 'price_cutoff': 154},
	'dress_shirt': {'categoryId': 57991, 'price_cutoff': 80},
	'casual_shirt': {'categoryId': 57990, 'price_cutoff': 89},
	'tie': {'categoryId': 15662, 'price_cutoff': 76},
	'sweater': {'categoryId': 11484, 'price_cutoff': 255},
	'coats_and_jacket': {'categoryId': 57988, 'price_cutoff': 316},
	'pant': {'categoryId': 57989, 'price_cutoff': 106},
	'jeans': {'categoryId': 11483, 'price_cutoff': 111},
	'suit': {'categoryId': 3001, 'price_cutoff': 305},
	'vest': {'categoryId': 15691, 'price_cutoff': 79},
	'sleepwear_and_robe': {'categoryId': 11510, 'price_cutoff': 143},
	'dress_shoes': {'categoryId': 53120, 'price_cutoff': 520}
}

items_master_list = []

for cat, data in category_ids_and_price_cutoff.items():
	executed_api = return_executed_call_for_category(
		f_api,
		data['categoryId'],
		min_price=data['price_cutoff'],
		min_bids=10
	)['connection']
	# print(executed_api)
	if int(executed_api.response.dict()['paginationOutput']['totalEntries']) > 0:
		cat_items = depaginate_item_search_results(executed_api)
		items_master_list.extend(cat_items)
	else:
		print('No listings for <{}>'.format(cat))
		# print(executed_api.response.dict())

print(items_master_list)
print(len(items_master_list))

template = jinja_env.get_template('base_forum_post.txt')
print(template.render(items=items_master_list))



