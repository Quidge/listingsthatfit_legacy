from app.ebay2db import lookup_and_add_new_items as lookup
from ebaysdk.finding import Connection as Finding

fapi = Finding(
	domain="svcs.ebay.com",
	appid="***REMOVED***",
	config_file=None,
	debug=False
)

lookup(fapi, 'balearic1')