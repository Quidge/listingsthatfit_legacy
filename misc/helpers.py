import json
import os

from urllib import request, parse

endpoint = "http://svcs.ebay.com/services/search/FindingService/v1"
api_key = os.environ['EBAY_PRODUCTION_APP_ID']


def get_env_variable(name):
	try:
		return os.environ[name]
	except KeyError:
		message = "Expected environment variable '{}' not set".format(name)
		raise Exception(message)

def findItemsByKeywords(endpoint, API_KEY, keywords, additionalVals=None):
	"""Takes an endpoint and a dict holding name=value pairs. Returns a JSON objectwith results.

	search() will do the URL encoding for you. 
	"""

	defaults = parse.urlencode({
		"OPERATION-NAME": "findItemsByKeywords",
		"SERVICE-VERSION": "1.0.0",
		"SECURITY-APPNAME": api_key,
		"GLOBAL-ID": "EBAY-US",
		"RESPONSE-DATA-FORMAT": "JSON"
	})

	url = endpoint + "?" + defaults + "&REST-PAYLOAD&" + parse.urlencode(keywords, quote_via=parse.quote)
	if additionalVals:
		url += "&" + parse.urlencode(additionalVals, quote_via=parse.quote)

	return request.urlopen(url)

def findItemsAdvanced(endpoint, API_KEY, keywords, as_json=False):
	"""Takes an endpoint and a dict holding name=value pairs. Returns a JSON objectwith results.

	search() will do the URL encoding for you. 
	"""

	defaults = parse.urlencode({
		"OPERATION-NAME": "findItemsAdvanced",
		"SERVICE-VERSION": "1.0.0",
		"SECURITY-APPNAME": api_key,
		"GLOBAL-ID": "EBAY-US",
		"RESPONSE-DATA-FORMAT": "JSON"
	})

	url = endpoint + "?" + defaults + "&REST-PAYLOAD&" + parse.urlencode(keywords, quote_via=parse.quote)

	resp = request.urlopen(url)

	if as_json:
		return json.loads(resp.read())
	else:
		return request.urlopen(url)

def findItemsBySeller(endpoint, API_KEY, sellerName, keywords={}, as_json=False):
	"""Helper function that wraps findItemsAdvanced and adds sellerName as key"""

	keywords["itemFilter.name"] = "Seller"
	keywords["itemFilter.value"] = sellerName

	return findItemsAdvanced(endpoint, API_KEY, keywords, as_json)
