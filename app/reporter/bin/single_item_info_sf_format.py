import sys
from app.reporter.generate import single_item_measurements_report as gen

if len(sys.argv) != 2:
	print('Usage: scriptname <ebay_item_id>')
else:
	report = gen(sys.argv[1])
	print(report)
