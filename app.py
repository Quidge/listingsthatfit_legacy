import json

from helpers import findItemsByKeywords, findItemsAdvanced, findItemsBySeller

endpoint = "http://svcs.ebay.com/services/search/FindingService/v1"
api_key = "***REMOVED***"

limit10 = {
	"paginationInput.entriesPerPage": 5,
}

resp = findItemsBySeller(endpoint, api_key, 'balearic1', keywords=limit10)

print(json.dumps(json.loads(resp.read()), indent=4))