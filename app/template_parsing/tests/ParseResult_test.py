import os
import pytest
from app.template_parsing import ParseResult, Measurement as Msmt


@pytest.fixture()
def dehydrated_ParseResult_from_json_file():
	with open(os.path.dirname(__file__) + '/sample_ParseResult_instance_as_json.json', 'r') as json_file:
		yield json_file.read()


@pytest.fixture()
def adhoc_ParseResult():
	p = ParseResult()
	p.clothing_type = 'pant'
	p.meta = {
		'parse_strategy': 'default',
		'concerns': [],
		'parsed_html': '<table cellpadding="0" cellspacing="0" style="font-size: inherit; ">\n<tbody><tr><td class="head" colspan="2"><h3>Approximate Measurements</h3></td></tr>\n<tr>\n<td>Across Waist</td>\n<td>15”</td></tr><tr><td>Across Hips</td>\n<td>18"</td>\n</tr>\n<tr>\n<td>Inseam</td>\n<td>28.5”\xa0</td>\n</tr>\n<tr>\n<td>Cuff Height</td>\n<td>0"</td>\n</tr><tr>\n<td>Material underneath hem</td>\n<td>2.25"</td>\n</tr><tr>\n<td>Width of hem opening</td>\n<td>9"</td>\n</tr><tr>\n<td>Rise</td>\n<td>9.75"</td></tr>\n</tbody></table>'
	}
	p.measurements = [
		Msmt(category='pant', attribute='waist_flat', measurement_value=15000),
		Msmt(category='pant', attribute='hips_flat', measurement_value=18000),
		Msmt(category='pant', attribute='inseam', measurement_value=28500),
		Msmt(category='pant', attribute='cuff_height', measurement_value=0),
		Msmt(category='pant', attribute='cuff_width', measurement_value=9000),
		Msmt(category='pant', attribute='rise', measurement_value=9750)]
	return p


@pytest.fixture()
def dehydrated_ParseResult():
	p = ParseResult()
	p.clothing_type = 'pant'
	p.meta = {
		'parse_strategy': 'default',
		'concerns': [],
		'parsed_html': '<table cellpadding="0" cellspacing="0" style="font-size: inherit; ">\n<tbody><tr><td class="head" colspan="2"><h3>Approximate Measurements</h3></td></tr>\n<tr>\n<td>Across Waist</td>\n<td>15”</td></tr><tr><td>Across Hips</td>\n<td>18"</td>\n</tr>\n<tr>\n<td>Inseam</td>\n<td>28.5”\xa0</td>\n</tr>\n<tr>\n<td>Cuff Height</td>\n<td>0"</td>\n</tr><tr>\n<td>Material underneath hem</td>\n<td>2.25"</td>\n</tr><tr>\n<td>Width of hem opening</td>\n<td>9"</td>\n</tr><tr>\n<td>Rise</td>\n<td>9.75"</td></tr>\n</tbody></table>'
	}
	p.measurements = [
		Msmt(category='pant', attribute='waist_flat', measurement_value=15000),
		Msmt(category='pant', attribute='hips_flat', measurement_value=18000),
		Msmt(category='pant', attribute='inseam', measurement_value=28500),
		Msmt(category='pant', attribute='cuff_height', measurement_value=0),
		Msmt(category='pant', attribute='cuff_width', measurement_value=9000),
		Msmt(category='pant', attribute='rise', measurement_value=9750)]
	return p.json()


def test_rehydrate_fails_when_passed_non_ParseResult_json():
	with pytest.raises(TypeError):
		ParseResult.rehydrate({'not': 'ParseResult_instance_json'})


def test_rehydrate_runs(dehydrated_ParseResult, dehydrated_ParseResult_from_json_file):
	ParseResult.rehydrate(dehydrated_ParseResult_from_json_file)
	ParseResult.rehydrate(dehydrated_ParseResult)


def test_rehydrate_returns_parse_result_type(adhoc_ParseResult):
	assert type(ParseResult.rehydrate(adhoc_ParseResult.json())) is ParseResult


def test_rehydrate_is_lossless(adhoc_ParseResult):
	# Create two different objects
	a = ParseResult.rehydrate(adhoc_ParseResult.json())
	b = ParseResult.rehydrate(adhoc_ParseResult.json())
	assert a.clothing_type == b.clothing_type
	assert a.meta == b.meta
	# a simple equality a.measurements == b.measurements check doesn't work for some reason
	for i, m in enumerate(a.measurements):
		assert m.category == b.measurements[i].category
		assert m.attribute == b.measurements[i].attribute
		assert m.value == b.measurements[i].value




