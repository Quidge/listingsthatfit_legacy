import pytest
from bs4 import BeautifulSoup

from ..core.director import get_sportcoat_measurements
from ..core.director import get_suit_measurements
from ..core.director import get_sweater_measurements
from ..core.director import get_pant_measurements
from ..core.director import get_casual_shirt_measurements
from ..core.director import get_dress_shirt_measurements
from ..core.director import get_coat_and_jacket_measurements
from ..core.director import director

from app.template_parsing.exception import (
	UnrecognizedMeasurement,
	UnsupportedParsingStrategy,
	UnsupportedClothingCategory,
	UnrecognizedTemplateHTML)


def test_returns_appropriate_parse_function():
	assert director('sportcoat') is get_sportcoat_measurements
	assert director('suit') is get_suit_measurements
	assert director('sweater') is get_sweater_measurements
	assert director('pant') is get_pant_measurements
	assert director('casual_shirt') is get_casual_shirt_measurements
	assert director('dress_shirt') is get_dress_shirt_measurements
	assert director('coat_or_jacket') is get_coat_and_jacket_measurements


def test_raises_unsupported_category_correctly():
	with pytest.raises(UnsupportedClothingCategory):
		director('fail')


def test_fails_when_passed_unsupported_parsing_strategy():
	clothing_types = [
		'sportcoat', 'suit', 'sweater', 'pant',
		'casual_shirt', 'dress_shirt', 'coat_or_jacket']
	tokenHtml = '<token></token>'
	for clothing_type in clothing_types:
		parse_fn = director(clothing_type)
		with pytest.raises(UnsupportedParsingStrategy):
			parse_fn(BeautifulSoup(tokenHtml, 'html.parser'), parse_strategy='fail')


@pytest.fixture(scope='module')
def pant_measurements_table_soup():
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









