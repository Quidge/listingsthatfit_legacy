import os
import json
import pytest
from app.template_parsing import ParseResult, Measurement as Msmt


@pytest.fixture(scope='module')
def sample_ParseResult_json():
	with open(os.path.dirname(__file__) + '/sample_ParseResult_instance_as_json.json', 'r') as json_file:
		yield json.dumps(json.load(json_file))


@pytest.fixture()
def same_as_Parse_result_json():
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


def test_rehydrate_runs(sample_ParseResult_json):
	assert ParseResult().rehydrate(sample_ParseResult_json)


def test_rehydrate_returns_expected(sample_ParseResult_json, same_as_Parse_result_json):
	assert sample_ParseResult_json == same_as_Parse_result_json.json()

# def test_ParseResult_can_rehydrate():
	# with open(os.path.dirname(__file__) + '/sample_ParseResult_instance_as_json.json', 'r') as json_file:
		# assert ParseResult().rehydrate(json_file.read())


"""def test_ParseResult():
	d = {
				'clothing_type': 'pant',
				'measurements': [
					{'category': 'pant', 'attribute': 'waist_flat', 'value': 15000},
					{'category': 'pant', 'attribute': 'hips_flat', 'value': 18000},
					{'category': 'pant', 'attribute': 'inseam', 'value': 28500},
					{'category': 'pant', 'attribute': 'cuff_height', 'value': 0},
					{'category': 'pant', 'attribute': 'cuff_width', 'value': 9000},
					{'category': 'pant', 'attribute': 'rise', 'value': 9750}],
				'meta': {
					'parse_strategy': 'default',
					'concerns': [],
					'parsed_html': '<table cellpadding="0" cellspacing="0" style="font-size: inherit; ">\n<tbody><tr><td class="head" colspan="2"><h3>Approximate Measurements</h3></td></tr>\n<tr>\n<td>Across Waist</td>\n<td>15”</td></tr><tr><td>Across Hips</td>\n<td>18"</td>\n</tr>\n<tr>\n<td>Inseam</td>\n<td>28.5”\xa0</td>\n</tr>\n<tr>\n<td>Cuff Height</td>\n<td>0"</td>\n</tr><tr>\n<td>Material underneath hem</td>\n<td>2.25"</td>\n</tr><tr>\n<td>Width of hem opening</td>\n<td>9"</td>\n</tr><tr>\n<td>Rise</td>\n<td>9.75"</td></tr>\n</tbody></table>'
				}
		}
	ParseResult().rehydrate(json.dumps(d))"""
