import pytest
import json
import os

from ..parse import parse
from app.template_parsing import ParseResult


@pytest.fixture(scope='module')
def sample_api_res_dict():
	"""Yields the json file to be compared against"""
	# https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code
	with open(os.path.dirname(__file__) + '/tests/sample_api_res.json', 'r') as json_file:
		yield json.load(json_file)


def test_parse_returns_parse_result_type(sample_api_res):
	parsed = parse(json.dumps(sample_api_res))
	assert type(parsed) is ParseResult

