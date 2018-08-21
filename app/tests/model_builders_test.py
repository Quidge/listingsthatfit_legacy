import json
import os
import pytest
import app.model_builders
import datetime
from app.models import EbaySeller, Item, ClothingCategory, ItemMeasurement


@pytest.fixture()
def sample_response_dict():
	with open(os.path.dirname(__file__) + '/model_builders_test_sample_response.json', 'r') as json_file:
		yield json.load(json_file)


def test_build_ebay_item_model_returns_as_expected(sample_response_dict):
	m = app.model_builders.build_ebay_item_model(
		sample_response_dict, ebay_seller_id='balearic1', attempt_parse=True)
	assert type(m) is Item
	assert type(m.ebay_title) is str
	assert m.ebay_title == 'NWT #1 MENSWEAR Sartoria Formosa Hardy Minnis Fresco Solid Navy Suit 50 52 A1P'
	assert type(m.end_date) is datetime.datetime
	assert m.end_date == datetime.datetime(2018, 8, 19, 22, 48, 59)
	assert type(m.ebay_item_id) is int
	assert m.ebay_item_id == 362410421416
	assert type(m.current_price) is int
	assert m.current_price == 90000
	assert type(m.primary_category_number) is int
	assert m.primary_category_number == 3001
	assert type(m.seller) is EbaySeller
	assert m.seller.ebay_seller_id == 'balearic1'
	assert type(m.assigned_clothing_category) is ClothingCategory
	assert m.assigned_clothing_category.clothing_category_name == 'suit'
	# Not checking that all the measurements are themselves are valid. That's tested for in the parsing module.
	assert len(m.measurements) > 0
	assert type(m.measurements[0]) is ItemMeasurement
