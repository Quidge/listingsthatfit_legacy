import pytest
# from sqlalchemy import or_, and_, between, func, table, column, alias
# from app.models import (
	# Item, ItemMeasurement as ItemMsmt, EbayItemCategory, MeasurementItemType,
	# MeasurementItemCategory, ClothingCategory)
from app.instance.utils import measurement_block_query_builder as block_builder, recurse_construction_schema as recurse
from app.instance.query.matching_ad_hoc import MeasurementQueryParameter as MQP


@pytest.fixture()
def sample_sweater_config_without_schema():
	return {
		'sweater': {  # Sweaters
			'measurements_list': [
				MQP('sweater', 'chest_flat', 24250, 250),
				MQP('sweater', 'shoulders', 19625, 500),
				MQP('sweater', 'shoulders_raglan', 0, 0),
				MQP('sweater', 'sleeve', 26000, 1500),
				MQP('sweater', 'sleeve_from_armpit', 19250, 2000)
			],
			'required_count': 3,
			'construction_schema': None
		}
	}


@pytest.fixture()
def sample_sweater_config_with_schema():
	return {
		'sweater': {  # Sweaters
			'measurements_list': [
				MQP('sweater', 'chest_flat', 24250, 250),
				MQP('sweater', 'shoulders', 19625, 500),
				MQP('sweater', 'shoulders_raglan', 0, 0),
				MQP('sweater', 'sleeve', 26000, 1500),
				MQP('sweater', 'sleeve_from_armpit', 19250, 2000)
			],
			'required_count': 3,
			'construction_schema': ('and', [
				('and', ('sweater', 'chest_flat')),
				('or', [
					('and', [('and', ('sweater', 'shoulders')), ('and', ('sweater', 'sleeve'))]),
					('and', [('and', ('sweater', 'shoulders_raglan')), ('and', ('sweater', 'sleeve_from_armpit'))])
				])
			])
		}
	}


def test_block_builder_fails_if_passed_more_than_one_top_level_item_in_dict(sample_sweater_config_without_schema):
	additional_item = sample_sweater_config_without_schema
	additional_item['new_item'] = 'nothing'
	with pytest.raises(ValueError):
		block_builder(additional_item)


def test_block_builder_returns_as_expected_without_schema(sample_sweater_config_without_schema):
	clause = block_builder(sample_sweater_config_without_schema)
	assert str(clause.compile(compile_kwargs={'literal_binds': True})) == "clothing_category.clothing_category_name = 'sweater' AND measurement_item_category.measurement_item_category_name = 'sweater' AND measurement_item_type.measurement_item_type_name = 'chest_flat' AND item_measurement.item_measurement_value BETWEEN 24000 AND 24500 AND clothing_category.clothing_category_name = 'sweater' AND measurement_item_category.measurement_item_category_name = 'sweater' AND measurement_item_type.measurement_item_type_name = 'shoulders' AND item_measurement.item_measurement_value BETWEEN 19125 AND 20125 AND clothing_category.clothing_category_name = 'sweater' AND measurement_item_category.measurement_item_category_name = 'sweater' AND measurement_item_type.measurement_item_type_name = 'shoulders_raglan' AND item_measurement.item_measurement_value BETWEEN 0 AND 0 AND clothing_category.clothing_category_name = 'sweater' AND measurement_item_category.measurement_item_category_name = 'sweater' AND measurement_item_type.measurement_item_type_name = 'sleeve' AND item_measurement.item_measurement_value BETWEEN 24500 AND 27500 AND clothing_category.clothing_category_name = 'sweater' AND measurement_item_category.measurement_item_category_name = 'sweater' AND measurement_item_type.measurement_item_type_name = 'sleeve_from_armpit' AND item_measurement.item_measurement_value BETWEEN 17250 AND 21250"


def test_block_builder_returns_as_expected_with_schema(sample_sweater_config_with_schema):
	block_builder(sample_sweater_config_with_schema)


def test_recurse_construction_schema_works_with_simple():
	simple_instruction = ('and', ('sweater', 'sleeve_from_armpit'))
	simple_instruction_mqp_list = [MQP('sweater', 'sleeve_from_armpit', 19250, 2000)]
	mqp_dict = {}
	for mqp in simple_instruction_mqp_list:
		# This uses the mqp to build a tuple that can be used as the key for itself as a value
		mqp_dict[(mqp.category_name, mqp.type_name)] = mqp
	assert str(recurse(simple_instruction, mqp_dict, 'sweater')) == "clothing_category.clothing_category_name = :clothing_category_name_1 AND measurement_item_category.measurement_item_category_name = :measurement_item_category_name_1 AND measurement_item_type.measurement_item_type_name = :measurement_item_type_name_1 AND item_measurement.item_measurement_value BETWEEN :item_measurement_value_1 AND :item_measurement_value_2"


def test_recurse_construction_schema_works_with_complex():
	complex_instruction = ('and', [
		('and', ('sweater', 'chest_flat')),
		('or', [
			('and', [('and', ('sweater', 'shoulders')), ('and', ('sweater', 'sleeve'))]),
			('and', [('and', ('sweater', 'shoulders_raglan')), ('and', ('sweater', 'sleeve_from_armpit'))])
		])
	])
	complex_instruction_mqp_list = [
		MQP('sweater', 'chest_flat', 24250, 250),
		MQP('sweater', 'shoulders', 19625, 500),
		MQP('sweater', 'shoulders_raglan', 0, 0),
		MQP('sweater', 'sleeve', 26000, 1500),
		MQP('sweater', 'sleeve_from_armpit', 19250, 2000)
	]
	mqp_dict = {}
	for mqp in complex_instruction_mqp_list:
		# This uses the mqp to build a tuple that can be used as the key for itself as a value
		mqp_dict[(mqp.category_name, mqp.type_name)] = mqp
	assert str(recurse(complex_instruction, mqp_dict, 'sweater').compile(compile_kwargs={'literal_binds': True})) == "clothing_category.clothing_category_name = 'sweater' AND measurement_item_category.measurement_item_category_name = 'sweater' AND measurement_item_type.measurement_item_type_name = 'chest_flat' AND item_measurement.item_measurement_value BETWEEN 24000 AND 24500 AND (clothing_category.clothing_category_name = 'sweater' AND measurement_item_category.measurement_item_category_name = 'sweater' AND measurement_item_type.measurement_item_type_name = 'shoulders' AND item_measurement.item_measurement_value BETWEEN 19125 AND 20125 AND clothing_category.clothing_category_name = 'sweater' AND measurement_item_category.measurement_item_category_name = 'sweater' AND measurement_item_type.measurement_item_type_name = 'sleeve' AND item_measurement.item_measurement_value BETWEEN 24500 AND 27500 OR clothing_category.clothing_category_name = 'sweater' AND measurement_item_category.measurement_item_category_name = 'sweater' AND measurement_item_type.measurement_item_type_name = 'shoulders_raglan' AND item_measurement.item_measurement_value BETWEEN 0 AND 0 AND clothing_category.clothing_category_name = 'sweater' AND measurement_item_category.measurement_item_category_name = 'sweater' AND measurement_item_type.measurement_item_type_name = 'sleeve_from_armpit' AND item_measurement.item_measurement_value BETWEEN 17250 AND 21250)"
	# recurse(complex_instruction, mqp_dict, 'sweater', debug=True)
	# assert 0










