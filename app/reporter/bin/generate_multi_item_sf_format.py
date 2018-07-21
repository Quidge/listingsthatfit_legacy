import sys
from importlib import import_module

from app.instance.query.matching_ad_hoc import matching_in_categories_alt
from app.reporter.generate import generate_forum_post_w_msmts as gen
from app.models import Item
from app.reporter.utils import compile_item_with_measurements as compress

if len(sys.argv) != 2:
	raise ValueError('Usage: script_name <user_name>')

try:
	measurements_module = import_module('app.user_measurements.{}'.format(sys.argv[1]))
except ImportError:
	raise ImportError('Could not find module <app.user_measurements.{}>'.format(sys.argv[1]))

profile = measurements_module.mqp

item_list = matching_in_categories_alt(profile, with_measurements=True)

meta = {
	'total_search_count': Item.query.count(),
	'result_count': len(compress(item_list)),
	'measurements_provided': profile
}

report = gen(item_list, template='/styleforum/multi_item_w_msmts_mqps.txt', metadata=meta)
print(report)