import pytest
import os

from app.template_parsing import master_parse, ParseResult, Measurement


@pytest.fixture(scope='module')
def sample_inbound_json():
	"""Yields the json file to be compared against"""
	# https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code
	with open(os.path.dirname(__file__) + '/sample_inbound_json.json', 'r') as json_file:
		yield json_file.read()


def test_get_appropriate_seller_parse_fn_fails_when_passed_weird_shit():
	with pytest.raises(ImportError):
		master_parse.get_appropriate_seller_parse_fn('fail')


def test_parse_returns_expected_json(sample_inbound_json):
		result = master_parse.parse(sample_inbound_json)

		# This is an equivalent Parse result to what master_parse should return for
		# sample_inbound_json
		equivalent_pr = ParseResult()
		equivalent_pr.clothing_type = 'pant'
		equivalent_pr.meta = {
			'parse_strategy': 'default',
			'concerns': [],
			'parsed_html': '<table cellpadding="0" cellspacing="0" style="font-size: inherit; ">\n<tbody><tr><td class="head" colspan="2"><h3>Approximate Measurements</h3></td></tr>\n<tr>\n<td>Across Waist</td>\n<td>15”</td></tr><tr><td>Across Hips</td>\n<td>18"</td>\n</tr>\n<tr>\n<td>Inseam</td>\n<td>28.5”\xa0</td>\n</tr>\n<tr>\n<td>Cuff Height</td>\n<td>0"</td>\n</tr><tr>\n<td>Material underneath hem</td>\n<td>2.25"</td>\n</tr><tr>\n<td>Width of hem opening</td>\n<td>9"</td>\n</tr><tr>\n<td>Rise</td>\n<td>9.75"</td></tr>\n</tbody></table>'
		}
		equivalent_pr.measurements = [
			Measurement(category='pant', attribute='waist_flat', measurement_value=15000),
			Measurement(category='pant', attribute='hips_flat', measurement_value=18000),
			Measurement(category='pant', attribute='inseam', measurement_value=28500),
			Measurement(category='pant', attribute='cuff_height', measurement_value=0),
			Measurement(category='pant', attribute='cuff_width', measurement_value=9000),
			Measurement(category='pant', attribute='rise', measurement_value=9750)]
		assert equivalent_pr.json() == result
