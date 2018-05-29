from app.utils import str_dec_to_dec_type
from bs4 import BeautifulSoup


def get_sportcoat_measurements(html_template):
	"""Parses a sportcoat listing from seller balearic1 and returns the measurements
	as a dict.

	Parameters
	----------
	html_template : string

	Returns
	-------
	measurements_dict : dict
		Dictionary in form:
			{
				'chest': int,
				'sleeves': int,
				'shoulders': int,
				'waist': int,
				'boc': int
			}
			# All values are the decimal value included in
			# listing * 1000 and converted to integer
	"""

	soup = BeautifulSoup(html_template, 'html.parser')

	data = (
		soup
		.find(string='Approximate Measurements')  # string itself
		.parent  # enclosing <h3>
		.parent  # enclosing <td>
		.parent  # enclosing <tr>
		.parent  # enclosing <tbody>
		.parent  # enclosing <table>
	)

	tds = data.find_all('td')
	measurements_dict = {
		'chest': int(str_dec_to_dec_type(tds[2].string) * 1000),
		'sleeve': int(str_dec_to_dec_type(tds[4].string) * 1000),
		'shoulders': int(str_dec_to_dec_type(tds[6].string) * 1000),
		'waist': int(str_dec_to_dec_type(tds[8].string) * 1000),
		'boc': int(str_dec_to_dec_type(tds[10].string) * 1000)
	}

	return measurements_dict