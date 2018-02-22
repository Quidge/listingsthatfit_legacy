'''import json

from helpers import findItemsByKeywords, findItemsAdvanced, findItemsBySeller

endpoint = "http://svcs.ebay.com/services/search/FindingService/v1"
api_key = "***REMOVED***"

limit10 = {
	"paginationInput.entriesPerPage": 5,
}

resp = findItemsBySeller(endpoint, api_key, 'balearic1', keywords=limit10)
resp2 = findItemsBySeller(endpoint, api_key, 'balearic1', keywords=limit10, as_json=True)

#print(json.dumps(json.loads(resp.read())["findItemsAdvancedResponse"], indent=4))
print(json.dumps(resp2["findItemsAdvancedResponse"], indent=2))'''