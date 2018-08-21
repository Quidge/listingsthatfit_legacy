import logging
from ebaysdk.exception import PaginationLimit

logger = logging.getLogger(__name__)


def depaginate_search_result(connection):
	"""Depaginates a Finding connection that has been executed with a payload.

	Returns
	-------
	result : dict
		{'searchResult' : [list of items]}
	"""
	logger.info('Depaginating connection response')

	try:
		connection.response.dict()['searchResult']['item']
	except KeyError:
		raise ValueError(
			'Connection response does not appear to have any items\nResponse:\n%r' % (
				connection.response.reply,))

	result = {'searchResult': []}
	proceed = True
	while proceed:
		for item in connection.response.dict()['searchResult']['item']:
			result['searchResult'].append(item)
		logger.debug('Moving to next page')
		try:
			connection.next_page()
		except PaginationLimit:
			logger.debug('Reached PaginationLimit. Returning result.')
			proceed = False
	return result
