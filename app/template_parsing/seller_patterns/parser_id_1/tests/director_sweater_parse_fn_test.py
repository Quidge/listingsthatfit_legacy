import copy
import pytest
from bs4 import BeautifulSoup

from ..core.director import director

from app.template_parsing.exception import (
	UnrecognizedMeasurement,
	UnsupportedParsingStrategy,
	UnsupportedClothingCategory,
	UnrecognizedTemplateHTML)
from ..clothing_type_directory import supported_category_names as nm

TESTING_CLOTHING_TYPE = nm['SWEATER']


@pytest.fixture(scope='module')
def parse_fn():
	return director(TESTING_CLOTHING_TYPE)


@pytest.fixture(scope='module')
def measurements_table_soup():
	return BeautifulSoup("""
		<table cellpadding="0" cellspacing="0">
		<tbody><tr><td class="head" colspan="2"><h3>Approximate Measurements</h3></td></tr>
		<tr>
		<td>Pit to pit</td>
		<td>25.25"</td>
		</tr>
		<tr>
		<td>Sleeves from shoulder seam</td>
		<td>27.25"</td>
		</tr>
		<tr>
		<td>Shoulder seams across</td>
		<td>19"</td>
		</tr>
		<tr><td>Total Length </td>
		<td>27.75"</td>
		</tr><tr>
		</tr></tbody></table>""", 'html.parser')


def test_parse_fn_raises_unrecognized_template_html(
	parse_fn, measurements_table_soup):
	# remove one of the measurements from the passed soup
	copied = copy.copy(measurements_table_soup)
	copied.find_all('td')[2].decompose()
	with pytest.raises(UnrecognizedTemplateHTML):
		parse_fn(copied, 'default')
