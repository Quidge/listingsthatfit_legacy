# from app.ebay2db import lookup_and_add_new_items as lookup
from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping

fapi = Finding(
	domain="svcs.ebay.com",
	appid="***REMOVED***",
	config_file=None,
	debug=False
)

sapi = Shopping(
	domain="open.api.ebay.com",
	appid="***REMOVED***",
	config_file=None,
	debug=False
)

payload = {
	'itemFilter': [
		{'name': 'Seller', 'value': 'balearic1'},
		{'name': 'listingType', 'value': 'Auction'}
	],
	'categoryId': [3002]
}

# items = lookup(fapi, sapi, 'balearic1', with_measurements=True, custom_payload=payload)
# print(type(items))

### Test
# from app.ebay2db.core import lookup_single_item as lookup
# from app.template_parsing.seller_patterns.parser_id_1 import get_sportcoat_measurements as get_msmts


# print(items)

from app.model_builders import gather_measurement_models_from_html_desc as parse
from app.ebay2db.core import lookup_single_item
from bs4 import BeautifulSoup as BS

res = lookup_single_item(sapi, 352386131604, with_description=True)
# print(res.dict())

desc = res.dict()['Item']['Description']

[print(m.measurement_type.clothing_category, m.measurement_type.attribute, m.measurement_value) for m in parse(desc, 3001, 1)]





# parse(res.dict()[, ebay_category_id, parser_file_num)
