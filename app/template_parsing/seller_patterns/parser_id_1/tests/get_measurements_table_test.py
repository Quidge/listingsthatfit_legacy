from bs4 import BeautifulSoup
import os
import json
import pytest

from app.template_parsing.exception import UnrecognizedTemplateHTML
from ..core.get_measurements_table import get_measurements_table


def test_can_return_str():
	with open(os.path.dirname(__file__) + '/sample_api_res.json', 'r') as f:
		truth = json.load(f)
		msmts_table = get_measurements_table(
			truth["Item"]["Description"],
			output_fmt='string')
		assert type(msmts_table) is str


def test_fails_without_approximate_string():
	with pytest.raises(UnrecognizedTemplateHTML):
		get_measurements_table('<table>randy<span>ass</span>html</table>')


def test_can_return_soup():
	with open(os.path.dirname(__file__) + '/sample_api_res.json', 'r') as f:
		truth = json.load(f)
		msmts_table = get_measurements_table(
			truth["Item"]["Description"],
			output_fmt='soup')
		assert type(msmts_table) is BeautifulSoup


def test_finds_table():
	with open(os.path.dirname(__file__) + '/sample_api_res.json', 'r') as f:
		truth = json.load(f)
		msmts_table = get_measurements_table(
			truth["Item"]["Description"],
			output_fmt='string')
		assert msmts_table[:6] == '<table' and msmts_table[-8:] == '</table>'
