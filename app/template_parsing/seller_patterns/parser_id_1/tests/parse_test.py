import pytest
import json
import os

from ..parse import parse, simple_preparse_response_check as preparse_check
from app.template_parsing import ParseResult


@pytest.fixture(scope='module')
def sample_api_res_dict():
	"""Yields the json file to be compared against"""
	# https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code
	with open(os.path.dirname(__file__) + '/sample_api_res.json', 'r') as json_file:
		yield json.load(json_file)


@pytest.fixture()
def parse_result(sample_api_res_dict):
	result = parse(json.dumps(sample_api_res_dict))
	return result


def test_parse_returns_parse_result_type(parse_result):
	assert type(parse_result) is ParseResult


def test_parse_returns_correct_dict(parse_result):
	assert parse_result.dict() == {
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


def test_preparse_check_works_as_expected(sample_api_res_dict):
	preparse_check(sample_api_res_dict)


def test_preparse_check_fails_with_ack_failure():
	with pytest.raises(ValueError):
		preparse_check({'Ack': 'Failure'})


def test_preparse_check_fails_without_ack():
	with pytest.raises(KeyError):
		preparse_check({'no': 'ack'})

def test_preparse_check_fails_without_Item():
	with pytest.raises(KeyError):
		preparse_check({'Ack': 'Success', 'no': 'Item'})



