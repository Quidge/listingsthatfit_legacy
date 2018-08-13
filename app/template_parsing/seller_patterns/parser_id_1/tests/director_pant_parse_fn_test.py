import copy
import pytest
from bs4 import BeautifulSoup

from ..core.director import director

from app.template_parsing.exception import (
	UnrecognizedMeasurement,
	UnsupportedParsingStrategy,
	UnsupportedClothingCategory,
	UnrecognizedTemplateHTML)

TESTING_CLOTHING_TYPE = 'pant'


@pytest.fixture(scope='module')
def parse_fn():
	return director(TESTING_CLOTHING_TYPE)


@pytest.fixture(scope='module')
def measurements_table_soup():
	return BeautifulSoup("""
		<table cellpadding="0" cellspacing="0" style="font-size: inherit; ">
		<tbody><tr><td class="head" colspan="2"><h3>Approximate Measurements</h3></td></tr>
		<tr>
		<td>Across Waist</td>
		<td>15”</td></tr><tr><td>Across Hips</td>
		<td>18"</td>
		</tr>
		<tr>
		<td>Inseam</td>
		<td>28.5” </td>
		</tr>
		<tr>
		<td>Cuff Height</td>
		<td>0"</td>
		</tr><tr>
		<td>Material underneath hem</td>
		<td>2.25"</td>
		</tr><tr>
		<td>Width of hem opening</td>
		<td>9"</td>
		</tr><tr>
		<td>Rise</td>
		<td>9.75"</td></tr>
		</tbody></table>""", 'html.parser')


def test_parse_fn_raises_unrecognized_template_html(
	parse_fn, measurements_table_soup):
	# remove one of the measurements from the passed soup
	copied = copy.copy(measurements_table_soup)
	copied.find_all('td')[2].decompose()
	with pytest.raises(UnrecognizedTemplateHTML):
		parse_fn(copied, 'default')
