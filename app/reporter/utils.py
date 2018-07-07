def compile_item_with_measurements(results_list):
	"""Takes a results list that has both Item and ItemMeasurement instances and
	collapses them to a dictionary form.

	Returns
	-------
	item_dict : dict
	"""

	items_dict = {}

	for item, msmt in results_list:
		items_dict[item.ebay_item_id] = {'item_details': item, 'measurements': []}
	# print(results_list.count())
	for item, msmt in results_list:
		items_dict[item.ebay_item_id]['measurements'].append(msmt)
	return items_dict
