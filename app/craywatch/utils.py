from craywatch.core.analyze import return_list_of_prices
from craywatch.core.completed import request_completed
from craywatch import finding_connection as f_api


def get_prices(kth_percentile=None):
	categories = {
		'sportcoat': 3002,
		'dress_shirt': 57991,
		'casual_shirt': 57990,
		'tie': 15662,
		'sweater': 11484,
		'coats_and_jacket': 57988,
		'pant': 57989,
		'jeans': 11483,
		'suit': 3001,
		'vest': 15691,
		'sleepwear_and_robe': 11510,
		'swimwear': 15690,
		'dress_shoes': 53120,
	}

	prices = {}
	for key, category_id in categories.items():
		request_completed(category_id=category_id)

		num_sold = f_api.response.dict()['paginationOutput']['totalEntries']
		values_list = return_list_of_prices(f_api)
		list_len = len(values_list)
		list_mean = sum(values_list) / list_len

		prices[key] = {
			'average_price': list_mean,
			'values_list': values_list,
			'num_sold': num_sold
		}
		if kth_percentile is not None:
			from decimal import Decimal, Context
			kth_decimal = Decimal(kth_percentile) / 100
			index = Decimal(Decimal(list_len) * kth_decimal, Context(rounding='ROUND_UP'))
			sorted_values = sorted(values_list)
			kth_dist_value = sorted_values[int(index)]
			prices[key]['percentile'] = {
				'percentile_value': kth_percentile,
				'kth_distribution': kth_dist_value}

	'''
	prices = {}
	request_completed(category_id=3002)
	sportcoat_prices_list = return_list_of_prices(f_api)
	sportcoat_avg = sum(sportcoat_prices_list) / len(sportcoat_prices_list)
	
	request_completed(category_id=57991)
	dress_shirt_prices_list = return_list_of_prices(f_api)
	dress_shirt_avg = sum(dress_shirt_prices_list) / len(dress_shirt_prices_list)

	request_completed(category_id=15662)
	tie_prices_list = return_list_of_prices(f_api)
	tie_avg = sum(tie_prices_list) / len(tie_prices_list)

	request_completed(category_id=11484)
	sweater_prices_list = return_list_of_prices(f_api)
	sweater_avg = sum(sweater_prices_list) / len(sweater_prices_list)

	request_completed(category_id=57988)
	coats_prices_list = return_list_of_prices(f_api)
	coats_avg = sum(coats_prices_list) / len(coats_prices_list)

	request_completed(category_id=57989)
	pants_prices_list = return_list_of_prices(f_api)
	pants_avg = sum(pants_prices_list) / len(pants_prices_list)

	request_completed(category_id=3001)
	suits_prices_list = return_list_of_prices(f_api)
	'''

	return prices


data = get_prices(kth_percentile=90)

for category, datum in data.items():
	print('category: {} | items sold: {} | mean price: {} | value at .{} percentile: {} '.format(
		category, datum['num_sold'], datum['average_price'],
		datum['percentile']['percentile_value'], datum['percentile']['kth_distribution'])
	)


