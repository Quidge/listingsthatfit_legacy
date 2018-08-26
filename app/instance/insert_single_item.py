from json import loads, dumps
from app.instance import shopping_connection as s_api
from app.model_builders import build_ebay_item_model

item_id = 362353925503

#r = s_api.execute('GetSingleItem', {'ItemID': item_id})
#r_json = r.json()
#print(r_json)

def get_item_and_build_model(ebay_item_id, with_measurements=False, ebay_seller_id='balearic1'):
	response = get_item(ebay_item_id, with_measurements=with_measurements)
	model = build_ebay_item_model(
		loads(response),
		ebay_seller_id=ebay_seller_id,
		with_measurements=with_measurements)
	return model

def ad_hoc_parse_measurements():
	item = loads(get_item(362353898404, with_measurements=True))
	import app.template_parsing.seller_patterns.parser_id_1 as spoo_parser
	msmts = spoo_parser.get_suit_measurements(item['Item']['Description'], parse_strategy='smartv1')
	print(msmts)
	return msmts

# ad_hoc_parse_measurements()

# m = get_item_and_build_model(362353898404, with_measurements=True, ebay_seller_id='balearic1')
# from app import db
# db.session.add(m)
# db.session.commit()
# print(m.measurements)
