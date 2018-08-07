from bs4 import BeautifulSoup
from app.template_parsing.exception import UnrecognizedTemplateHTML
import logging

logger = logging.getLogger(__name__)


def get_measurements_table(html_description, output_fmt='soup'):
	"""Tries to find measurements table.

	Parameters
	----------
	html_description : str
	output_fmt='soup' : determines the return format

	Returns
	-------
	measurements_table : str / BeautifulSoup object
		The returned str or BS object is ONLY the measurements table. This should
		save performance.
	"""

	soup = BeautifulSoup(html_description, 'html.parser')
	logger.debug('Searching for "Approximate Measurements" table')
	try:
		assert soup.find(string='Approximate Measurements') is not None
	except AssertionError:
		logger.warn('Unable to find "Approximate Measurements" string in HTML')
		raise UnrecognizedTemplateHTML(
			'Unable to find "Approximate Measurements" string in HTML description',
			html_string=str(soup))
	else:
		ap = str(
			soup
			.find(string='Approximate Measurements')  # string itself
			.parent  # enclosing <h3>
			.parent  # enclosing <td>
			.parent  # enclosing <tr>
			.parent  # enclosing <tbody>
			.parent  # enclosing <table>
		)

	logger.debug('Found "Approximate Measurements" table')
	if output_fmt == 'soup':
		return BeautifulSoup(ap, 'html.parser')
	elif output_fmt == 'string':
		return ap
	else:
		raise ValueError('Unexpected parameter: fmt="{}"'.format(fmt))
