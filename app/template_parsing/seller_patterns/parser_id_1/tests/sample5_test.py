import json
import pytest
import os

from app.template_parsing import IdentifyResult
from ..core.identify_clothing_type import identify_clothing_type as identify
from ..core.get_measurements_table import get_measurements_table


@pytest.fixture(scope='module')
def comparison_result():
  """Yields the json file to be compared against"""
  # https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code
  with open(os.path.dirname(__file__) + '/sample5.json', 'r') as json_file:
    yield json.load(json_file)


@pytest.fixture(scope='module')
def ebay_primary_category_id(comparison_result):
  return int(comparison_result["response"]["Item"]["PrimaryCategoryID"])


@pytest.fixture(scope='module')
def measurements_table(comparison_result):
  """Yields the measurements table to be tested"""
  return get_measurements_table(
    comparison_result["response"]["Item"]["Description"],
    output_fmt="soup")


@pytest.fixture(scope='module')
def identify_result(measurements_table, ebay_primary_category_id):
  return identify(measurements_table, ebay_primary_category_id=ebay_primary_category_id)


def test_identify_returns_IdentifyResult_class(identify_result, comparison_result):
  assert type(identify_result) is IdentifyResult


def test_identify_returns_correct_clothing_type(identify_result, comparison_result):
  assert identify_result.identified_clothing_type == comparison_result['clothing_type']


def test_identify_returns_correct_ebay_primary_category(identify_result, ebay_primary_category_id):
  assert identify_result.ebay_primary_category_id == ebay_primary_category_id


def test_identify_returns_correct_observations(identify_result, comparison_result):
  """Tests that identify returns correct observation entries"""
  assert identify_result.observations['pants_section_declaration'] == comparison_result['description_observations']['pants_section_declaration']
  assert identify_result.observations['mentions_cuff'] == comparison_result['description_observations']['mentions_cuff']
  assert identify_result.observations['waist_mentions'] == comparison_result['description_observations']['waist_mentions']
  assert identify_result.observations['mentions_sleeve'] == comparison_result['description_observations']['mentions_sleeve']
  assert identify_result.observations['mentions_length'] == comparison_result['description_observations']['mentions_length']
