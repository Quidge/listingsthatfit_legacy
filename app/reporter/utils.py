from app.models import ItemMeasurement, Item


def compile_item_with_measurements(results_list):
	"""Takes a results list that has both Item and ItemMeasurement instances and
	collapses them to a dictionary form.

	Returns
	-------
	item_dict : dict
	"""

	test_item, test_msmt = results_list[0]
	try:
		assert isinstance(test_item, Item)
	except AssertionError:
		raise TypeError(
			'First item in first row of result list is not an Item instance')
	try:
		assert isinstance(test_msmt, ItemMeasurement)
	except AssertionError:
		raise TypeError(
			'Second item in first row of result list is not an ItemMeasurement instance')

	items_dict = {}

	for item, msmt in results_list:
		items_dict[item.ebay_item_id] = {'item_details': item, 'measurements': []}
	for item, msmt in results_list:
		items_dict[item.ebay_item_id]['measurements'].append(msmt)
	return items_dict
