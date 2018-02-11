import json

from urllib import request, parse

#endpoint = "http://svcs.sandbox.ebay.com/services/search/FindingService/v1"
#api_key = "Jonathan-testapp-SBX-dbffbb2e5-006125e7"

def getJSON(endpoint, API_KEY, keywords):
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
	print(url+"\n")

	resp = request.urlopen(url)

	#print(resp.status)
	return parsed = json.loads(resp.read())
	#print(json.dumps(parsed, indent=4))
	#print(f.reason)
	#repr(f)

	

#getJSON(endpoint, api_key, {"keywords": "harry potter"})