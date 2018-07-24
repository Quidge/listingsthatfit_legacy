import sys
from app.reporter.generate import single_item_measurements_report as gen
from app.models import Item

if len(sys.argv) != 2:
	print('Usage: scriptname <ebay_item_id>')
else:
	report = gen(sys.argv[1])
	print(report)
