from bs4 import BeautifulSoup as BS
from app.instance import shopping_connection as sapi
from app.ebayapis.core.lookup import lookup_single_item
from app.model_builders import build_ebay_item_model


def get_listing_soup(ebay_item_id, how_much='msmt_table'):
	res = lookup_single_item(sapi, ebay_item_id, with_description=True)
	desc = res.dict()['Item']['Description']
	soup = BS(desc, 'html.parser')

	if how_much == 'all':
		return soup
	elif how_much == 'msmt_table':
		msmt_table = (
			soup
			.find(string='Approximate Measurements')  # string itself
			.parent  # enclosing <h3>
			.parent  # enclosing <td>
			.parent  # enclosing <tr>
			.parent  # enclosing <tbody>
			.parent  # enclosing <table>
		)
		return msmt_table
