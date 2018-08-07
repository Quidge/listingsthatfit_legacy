import pytest
import json
import os
from bs4 import BeautifulSoup

from app.template_parsing import IdentifyResult
from app.template_parsing.exception import UnrecognizedTemplateHTML
from ..core.identify_clothing_type import identify_clothing_type
from ..core.get_measurements_table import get_measurements_table


def test_get_measurements_table_can_return_str():
	with open(os.path.dirname(__file__) + '/sample_api_res.json', 'r') as f:
		truth = json.load(f)
		msmts_table = get_measurements_table(
			truth["Item"]["Description"],
			output_fmt='string')
		assert type(msmts_table) is str


def test_get_measurements_table_fails_without_approximate_string():
	with pytest.raises(UnrecognizedTemplateHTML):
		get_measurements_table('<table>randy<span>ass</span>html</table>')


def test_get_measurements_table_can_return_soup():
	with open(os.path.dirname(__file__) + '/sample_api_res.json', 'r') as f:
		truth = json.load(f)
		msmts_table = get_measurements_table(
			truth["Item"]["Description"],
			output_fmt='soup')
		assert type(msmts_table) is BeautifulSoup


def test_get_measurements_table_finds_table():
	with open(os.path.dirname(__file__) + '/sample_api_res.json', 'r') as f:
		truth = json.load(f)
		msmts_table = get_measurements_table(
			truth["Item"]["Description"],
			output_fmt='string')
		assert msmts_table[:6] == '<table' and msmts_table[-8:] == '</table>'


def test_identify_clothing_type_fails_w_str_argument():
	with pytest.raises(TypeError):
		identify_clothing_type('fail')


def test_identify_clothing_type_returns_correct_object_type():
	with open(os.path.dirname(__file__) + '/sample_api_res.json', 'r') as f:
		truth = json.load(f)
		msmts_table = get_measurements_table(
			truth["Item"]["Description"],
			output_fmt='soup')
		result = identify_clothing_type(msmts_table)
		assert type(result) is IdentifyResult
