from bs4 import BeautifulSoup
from app.utils import str_dec_to_dec_type
from app.template_parsing.utils import find_paired_measurement_value as paired_val
from app.template_parsing.utils import str_measurement_to_int as str2int


def get_sportcoat_measurements(html_description):
	"""Parses a sportcoat listing from seller balearic1 and returns the measurements
	as a dict.

	Parameters
	----------
	html_description : string

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

	soup = BeautifulSoup(html_description, 'html.parser')

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

def get_suit_measurements(html_description, parse_strategy='naive'):
	"""Parses a sportcoat listing from seller balearic1 and returns the measurements
	as a dict.

	Parameters
	----------
	html_description : string

	Returns
	-------
	m_dict : dict
		Dictionary in form:
			{
				'jacket_chest': int value or None,
				'jacket_sleeve': int value or None,
				'jacket_shoulders': int value or None,
				'jacket_waist': int value or None,
				'jacket_boc': int value or None,
				'pant_waist': int value or None,
				'pant_hips': int value or None,
				'pant_inseam': int value or None,
				'pant_cuff_height': int value or None,
				'pant_leg_opening': int value or None,
				'pant_rise': int value or None
			}
			# All values are the decimal value included in
			# listing * 1000 and converted to integer
	"""

	soup = BeautifulSoup(html_description, 'html.parser')

	data = (
		soup
		.find(string='Approximate Measurements')  # string itself
		.parent  # enclosing <h3>
		.parent  # enclosing <td>
		.parent  # enclosing <tr>
		.parent  # enclosing <tbody>
		.parent  # enclosing <table>
	)

	m_dict = {
		'jacket_chest': None,
		'jacket_sleeve': None,
		'jacket_shoulders': None,
		'jacket_waist': None,
		'jacket_boc': None,
		'pant_waist': None,
		'pant_hips': None,
		'pant_inseam': None,
		'pant_cuff_height': None,
		'pant_leg_opening': None,
		'pant_rise': None
	}

	if parse_strategy == 'naive':
		strings = list(data.stripped_strings)
		m_dict = {
			'jacket_chest': str2int(strings[2]),
			'jacket_sleeve': str2int(strings[4]),
			'jacket_shoulders': str2int(strings[6]),
			'jacket_waist': str2int(strings[8]),
			'jacket_boc': str2int(strings[10]),
			'pant_waist': str2int(strings[13]),
			'pant_hips': str2int(strings[15]),
			'pant_inseam': str2int(strings[17]),
			'pant_cuff_height': str2int(strings[19]),
			'pant_leg_opening': str2int(strings[23]),
			'pant_rise': str2int(strings[25])
		}
	elif parse_strategy == 'smartv1':
		import re
		look_for = [
			'Pit to pit',
			'Sleeves from shoulder seam',
			'Shoulder seams across',
			'Length from BOC',
			'Across Hips',
			'Cuff height',
			'Extra material under cuff',
			'At cuff',
			'sleeve',
			'shoulder',
			'waist',
			'boc',
			'inseam',
			'hips',
			'cuff',
			'leg opening',
			'rise']
		possible_pairs = {}
		for candidate in look_for:
			results = data.find_all(string=re.compile(candidate, flags=re.IGNORECASE))
			possible_pairs[candidate] = [str2int(s.parent.parent.find(string=re.compile('\d*\.?\d\"'))) for s in results]
		
		m_dict['jacket_chest'] = possible_pairs['pit to pit'][0]
		# Try sleeves
		if len(possible_pairs['Sleeves from shoulder seam']) > 0:
			m_dict['jacket_sleeve'] = possible_pairs['Sleeves from shoulder seam'][0]
		else:
			m_dict['jacket_sleeve'] = possible_pairs['sleeve'][0]
		
		# Try shoulders
		if len(possible_pairs['Shoulder seams across']) > 0:
			m_dict['jacket_shoulders'] = possible_pairs['Shoulder seams across'][0]
		else:
			m_dict['jacket_shoulders'] = min(possible_pairs['shoulder'])  # if multiple, shoulder msmt < sleeve msmt
		
		# Try BOC
		if len(possible_pairs['Length from BOC']) > 0:
			m_dict['jacket_boc'] = possible_pairs['Length from BOC'][0]
		else:
			m_dict['jacket_boc'] = possible_pairs['boc'][0]
		
		# No good identifiers for these yet.
		m_dict['jacket_waist'] = possible_pairs['waist'][0]
		m_dict['pant_waist'] = possible_pairs['waist'][1]

		# Try pant hips
		if len(possible_pairs['Across Hips']) > 0:
			m_dict['pant_hips'] = possible_pairs['Across Hips'][0]
		else:
			m_dict['pant_hips'] = possible_pairs['hips'][0]
		
		# Try leg opening
		if len(possible_pairs['At cuff']) > 0:
			m_dict['pant_leg_opening'] = possible_pairs['At cuff'][0]
		else:
			m_dict['pant_leg_opening'] = max(possible_pairs['cuff'])

		# Try cuff height. If he uses a different string I can't discern it from the others. 
		# The measurement will be null.
		if len(possible_pairs['Cuff height']) > 0:
			m_dict['pant_cuff_height'] = possible_pairs['Cuff height'][0]

		m_dict['pant_rise'] = possible_pairs['rise'][0]

		# raise ValueError('Smart parsing not yet implemented. Please pass kwarg "naive_parse" with <True>')

	else:
		raise ValueError(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))


	return m_dict











