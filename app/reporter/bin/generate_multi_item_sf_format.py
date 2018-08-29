import sys
import logging
import datetime
from importlib import import_module

from app.instance.query.matching_ad_hoc import matching_in_categories_alt
from app.reporter.generate import generate_forum_post_w_msmts as gen
from app.models import Item
from app.reporter.utils import compile_item_with_measurements as compress

if __name__ != '__main__':
	raise ValueError('This script is designed to be used as a cli program.')

logger = logging.getLogger('app.reporter.bin.generate_multi_item_sf_format')

if len(sys.argv) != 2:
	raise ValueError('Usage: script_name <user_name>')

logger.info('Starting generate_new_items_sf_format script.')
logger.info('Generating report for user={}'.format(sys.argv[1]))

try:
	measurements_module = import_module('app.user_measurements.{}'.format(sys.argv[1]))
except ImportError:
	raise ImportError('Could not find module <app.user_measurements.{}>'.format(sys.argv[1]))

profile = measurements_module.mqp

logger.info('Running query for items with provided user measurements')
item_list = matching_in_categories_alt(profile, with_measurements=True)

logger.info('Generating meta')
meta = {
	'total_search_count': Item.query.filter(
		Item.end_date > datetime.datetime.now()).count(),
	'result_count': len(compress(item_list)),
	'measurements_provided': profile
}

template = '/styleforum/multi_item_w_msmts_mqps.txt'

logger.info('Generating templated report using template: <%r>' % template)
report = gen(item_list, template=template, metadata=meta)
print(report)
