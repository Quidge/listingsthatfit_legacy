from json import loads, dumps

from ebaysdk.shopping import Connection as Shopping

from app.model_builders import build_ebay_item_model

prodEndpoint = "open.api.ebay.com"
prodAppId = "***REMOVED***"

s_api = Shopping(
	domain=prodEndpoint,
	appid=prodAppId,
	config_file=None,
	debug=False
)

item_id = 362353925503

#r = s_api.execute('GetSingleItem', {'ItemID': item_id})
#r_json = r.json()
#print(r_json)

def get_item():
	r = s_api.execute('GetSingleItem', {'ItemID': item_id})
	return r.json()
