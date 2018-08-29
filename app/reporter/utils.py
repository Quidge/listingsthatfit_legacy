import logging
from app.models import ItemMeasurement, Item

logger = logging.getLogger(__name__)


def compile_item_with_measurements(results_list):
	"""Takes a SQLAlechemy ResultList object that has both Item and ItemMeasurement
	instances and collapses them to a dictionary form.

	Returns
	-------
	item_dict : dict
	"""
	logger.info('Starting results list compressor')
	logger.debug('Found <%r> rows to compress' % results_list.count())
	# print(len(results_list))
	try:
		test_item, test_msmt = results_list[0]
	except IndexError:
		logger.debug('No items found in results_list. Compressor returning empty dict.')
		return {}  # Empty, and early, return
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

	logger.info((
		'Finished results list compressor. '
		'Returning dict with <{}> entries').format(len(items_dict)))
	return items_dict
