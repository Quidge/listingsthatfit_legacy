import copy
import pytest
from bs4 import BeautifulSoup

from ..core.director import director
from app.template_parsing import MeasurementsCollection
from app.template_parsing.exception import (
	UnrecognizedMeasurement,
	UnsupportedParsingStrategy,
	UnsupportedClothingCategory,
	UnrecognizedTemplateHTML)

TESTING_CLOTHING_TYPE = 'dress_shirt'


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
		<td>23"</td>
		</tr>
		<tr>
		</tr>
		<tr>
		<td>Sleeves from shoulder seam</td>
		<td>22.75"</td>
		</tr>
		<tr><td>Across shoulder seams</td>
		<td>20" </td>
		</tr><tr>
		</tr></tbody></table>""", 'html.parser')


def test_parse_fn_raises_unrecognized_template_html(
	parse_fn, measurements_table_soup):
	# remove one of the measurements from the passed soup
	copied = copy.copy(measurements_table_soup)
	copied.find_all('td')[2].decompose()
	with pytest.raises(UnrecognizedTemplateHTML):
		parse_fn(copied, 'default')


def test_parse_fn_returns_measurement_collection(
	parse_fn, measurements_table_soup):
	assert type(parse_fn(measurements_table_soup, 'default')) is MeasurementsCollection








