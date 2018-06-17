from .core.pull_items import request_items
from decimal import Decimal


min_price = 200.0
min_bids = 5

resp = request_items(min_price=min_price, min_bids=min_bids)

# print(items)

print('There are {} auctions with more than {} bids and currently at a price higher than {}'.format(
	resp['paginationOutput']['totalEntries'], min_bids, min_price))
print('$ Price | # Bids | Title')
print('------------------------')

for i in resp['searchResult']['item']:
	print('{} | {} | {}'.format(
		Decimal(i['sellingStatus']['currentPrice']['value']),
		i['sellingStatus']['bidCount'],
		i['title'])
	)
