import os

from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping

env_app_id = os.environ['EBAY_PRODUCTION_APP_ID']

finding_connection = Finding(
	domain="svcs.ebay.com",
	appid=env_app_id,
	config_file=None,
	debug=False)

shopping_connection = Shopping(
	domain="open.api.ebay.com",
	appid=env_app_id,
	config_file=None,
	debug=False
)
