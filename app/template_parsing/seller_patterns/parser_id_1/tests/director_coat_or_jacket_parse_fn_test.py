import pytest
from bs4 import BeautifulSoup

from ..core.director import director

from app.template_parsing.exception import (
	UnrecognizedMeasurement,
	UnsupportedParsingStrategy,
	UnsupportedClothingCategory,
	UnrecognizedTemplateHTML)

TESTING_CLOTHING_TYPE = 'coat_or_jacket'


@pytest.fixture(scope='module')
def parse_fn():
	return director(TESTING_CLOTHING_TYPE)


@pytest.fixture(scope='module')
def measurements_table_soup():
	return BeautifulSoup("""
		<table cellpadding="0" cellspacing="0" style="font-size: inherit; ">
		<tbody><tr><td class="head" colspan="2"><h3>Approximate Measurements</h3></td></tr>
		<tr>
		<td>Pit to pit</td>
		<td>21"</td>
		</tr>
		<tr>
		<td>Sleeves from shoulder seam</td>
		<td>32.5"</td>
		</tr>
		<tr>
		<td>Shoulder seams across</td>
		<td>17.75"</td>
		</tr>
		<tr>
		</tr><tr>
		<td>Length from bottom of collar</td>
		<td>25"</td>
		</tr><tr>
		</tr>
		</tbody></table>""", 'html.parser')


def test_parse_fn_raises_unrecognized_template_html(
	parse_fn, measurements_table_soup):
	# remove one of the measurements from the passed soup
	measurements_table_soup.find_all('td')[2].decompose()
	with pytest.raises(UnrecognizedTemplateHTML):
		parse_fn(measurements_table_soup, 'default')
