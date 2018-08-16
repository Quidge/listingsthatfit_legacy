import pytest
import json
import os

from app.template_parsing import master_parse


@pytest.fixture(scope='module')
def sample_inbound_json():
	"""Yields the json file to be compared against"""
	# https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code
	with open(os.path.dirname(__file__) + '/sample_inbound_json.json', 'r') as json_file:
		yield json_file


def test_parse_returns_expected_json():
	with open(os.path.dirname(__file__) + '/sample_inbound_json.json', 'r') as json_file:
		result = master_parse.parse(json_file.read())
		assert json.loads(result) == {
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
