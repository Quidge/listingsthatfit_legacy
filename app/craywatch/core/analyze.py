from decimal import Decimal

from ebaysdk.exception import PaginationLimit


def strip_prices_from_items_dict(items_dict, num_format='decimal'):
	prices = []
	if num_format == 'decimal':
		prices = [Decimal(i['sellingStatus']['currentPrice']['value']) for i in items_dict]
	elif num_format == 'integer':
		price = [int(Decimal(i['sellingStatus']['currentPrice']['value']) * 100) for i in items_dict]
	else:
		raise ValueError(
			'<num_format> arguement must be either "decimal" or "integer". Passed <{}>'.format(num_format))
	return prices


def return_list_of_prices(connection, price_format='decimal'):
	response = connection.response
	prices = []
	proceed = True
	while proceed:
		prices.extend(strip_prices_from_items_dict(
			response.dict()['searchResult']['item'],
			price_format))
		try:
			response = connection.next_page()
		except PaginationLimit:
			proceed = False
		# for item in conn.response.reply['searchResult']['item']:
			# price = Decimal(item['sellingStatus']['currentPrice']['value'])
			# prices.append(price)

	return prices
