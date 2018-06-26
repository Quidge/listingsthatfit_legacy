# from app.ebayapis import lookup_and_add_new_items as lookup
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
# from app.ebayapis.core import lookup_single_item as lookup
# from app.template_parsing.seller_patterns.parser_id_1 import get_sportcoat_measurements as get_msmts


# print(items)

# from app.model_builders import gather_measurement_models_from_html_desc as parse
from app.ebayapis.core import lookup_single_item

res = lookup_single_item(sapi, 3, with_description=True)

# desc = res.dict()['Item']['Description']

'''for m in parse(desc, 3001, 1):
	print(
		m.measurement_type.clothing_category,
		m.measurement_type.attribute,
		m.measurement_value)'''




