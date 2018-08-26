import os
from ebaysdk.finding import Connection as Finding
from jinja2 import Environment, PackageLoader

jinja_env = Environment(
	loader=PackageLoader('craywatch', 'templates')
)

env_app_id = os.environ['EBAY_PRODUCTION_APP_ID']

finding_connection = Finding(
	domain="svcs.ebay.com",
	appid=env_app_id,
	config_file=None,
	debug=False)

ebay_category_ids = {
	'sportcoat': 3002,
	'dress_shirt': 57991,
	'casual_shirt': 57990,
	'tie': 15662,
	'sweater': 11484,
	'coats_and_jacket': 57988,
	'pant': 57989,
	'jeans': 11483,
	'suit': 3001,
	'vest': 15691,
	'sleepwear_and_robe': 11510,
	'swimwear': 15690,
	'dress_shoes': 53120
}
