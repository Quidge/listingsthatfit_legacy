import pytest
import json
import os

from app.template_parsing import IdentifyResult
from ..core.identify_clothing_type import identify_clothing_type
from ..core.get_measurements_table import get_measurements_table


def test_identify_clothing_type_fails_w_str_argument():
	with pytest.raises(TypeError):
		identify_clothing_type('fail')


def test_identify_clothing_type_returns_correct_object_type():
	with open(os.path.dirname(__file__) + '/sample_api_res.json', 'r') as f:
		truth = json.load(f)
		msmts_table = get_measurements_table(
			truth["Item"]["Description"],
			output_fmt='soup')
		result = identify_clothing_type(msmts_table)
		assert type(result) is IdentifyResult
