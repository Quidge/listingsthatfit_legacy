import copy
import pytest
from bs4 import BeautifulSoup
from app.template_parsing import Measurement as Msmt

from ..core.director import director

from app.template_parsing.exception import (
	UnrecognizedMeasurement,
	UnsupportedParsingStrategy,
	UnsupportedClothingCategory,
	UnrecognizedTemplateHTML)
from ..clothing_type_directory import supported_category_names as nm

TESTING_CLOTHING_TYPE = nm['COAT_OR_JACKET']


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

@pytest.fixture(scope='module')
def measurements_table_soup_raglan():
	return BeautifulSoup("""
		<table cellpadding="0" cellspacing="0" style="font-size: inherit; ">
		<tbody><tr><td class="head" colspan="2"><h3>Approximate Measurements</h3></td></tr>
		<tr>
		<td>Pit to pit</td>
		<td>21"</td>
		</tr>
		<tr>
		<td>Sleeves from underarm seam</td>
		<td>19"</td>
		</tr>
		<tr>
		<td>Shoulder seams across</td>
		<td>NA/Raglan</td>
		</tr>
		<tr>
		</tr><tr>
		<td>Length from bottom of collar</td>
		<td>23"</td>
		</tr><tr>
		</tr>
		</tbody></table>""", 'html.parser')


def test_parse_fn_raises_unrecognized_template_html(
	parse_fn, measurements_table_soup):
	# remove one of the measurements from the passed soup
	copied = copy.copy(measurements_table_soup)
	copied.find_all('td')[2].decompose()
	with pytest.raises(UnrecognizedTemplateHTML):
		parse_fn(copied, 'default')


def test_parse_fn_finds_raglan(parse_fn, measurements_table_soup_raglan):
	raglan_jacket_parse = parse_fn(measurements_table_soup_raglan, 'default')
	measurements = raglan_jacket_parse.measurements_list
	# Check to see if these Measurement instances are in the measurements list
	assert any([measurement.__dict__ == Msmt('jacket', 'sleeve_from_armpit', 19000).__dict__ for measurement in measurements]) is True
	assert any([measurement.__dict__ == Msmt('jacket', 'shoulders_raglan', 0).__dict__ for measurement in measurements]) is True
	# Check to be sure shoulders and normal sleeve measurements are NOT in the list
	assert any([measurement.attribute == 'shoulders' for measurement in measurements]) is False
	assert any([measurement.attribute == 'sleeve' for measurement in measurements]) is False



