import os

from ebaysdk.shopping import Connection as Shopping
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

f_prodEndpoint = "svcs.sandbox.ebay.com"
s_prodEndpoint = "open.api.ebay.com"
try:
	prodAppId = os.environ['EBAY_PRODUCTION_APP_ID']
except KeyError:
	raise KeyError('Cannot find EBAY_PRODUCTION_APP_ID in environment')


f_api = Finding(
	domain=f_prodEndpoint,
	appid=prodAppId,
	config_file=None,
	debug=False
)

s_api = Shopping(
	domain=s_prodEndpoint,
	appid=prodAppId,
	config_file=None,
	debug=False
)

f_payload = {
	'categoryId': 3002,
	'itemFilter': {'name': 'Seller', 'value': 'balearic1'},
}

try:
	f_resp = f_api.execute('findItemsAdvanced', f_payload)
except ConnectionError:
	raise ConnectionError('Finding Api failed to connect')

print(f_resp.dict())

