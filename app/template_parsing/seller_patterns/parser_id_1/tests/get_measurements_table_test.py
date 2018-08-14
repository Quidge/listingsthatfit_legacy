from bs4 import BeautifulSoup
import os
import json
import pytest

from app.template_parsing.exception import UnrecognizedTemplateHTML
from ..core.get_measurements_table import get_measurements_table


def test_fails_without_approximate_string():
	with pytest.raises(UnrecognizedTemplateHTML):
		get_measurements_table('<table>randy<span>ass</span>html</table>')


@pytest.fixture
def html_description(scope='module'):
	with open(os.path.dirname(__file__) + '/sample_api_res.json', 'r') as f:
		yield json.load(f)['Item']['Description']


def test_can_return_str(html_description):
	msmts_table = get_measurements_table(
		html_description,
		output_fmt='string')
	assert type(msmts_table) is str


def test_can_return_soup(html_description):
	msmts_table = get_measurements_table(
		html_description,
		output_fmt='soup')
	assert type(msmts_table) is BeautifulSoup


def test_finds_table(html_description):
	msmts_table = get_measurements_table(
		html_description,
		output_fmt='string')
	assert msmts_table[:6] == '<table' and msmts_table[-8:] == '</table>'
