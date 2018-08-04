import re
import logging
from bs4 import BeautifulSoup
# from app.template_parsing.utils import find_paired_measurement_value as paired_val
from app.template_parsing.utils import str_measurement_to_int as str2int
from app.template_parsing.utils import find_paired_measurement_value as get_paired_msmt
from app.template_parsing import MeasurementsCollection
from app.template_parsing import Measurement as Msmt
from app.template_parsing import ParseParameter as PP
from app.template_parsing.exception import UnsupportedParsingStrategy, UnrecognizedMeasurement, UnrecognizedTemplateHTML


##########################
## Parser for SpooPoker ##
##########################

logger = logging.getLogger(__name__)


def get_sportcoat_measurements(html_description, parse_strategy='default'):
	"""Parses a sportcoat listing from seller balearic1 and returns the measurements
	as a dict.

	Parameters
	----------
	html_description : str
	parse_strategy : str
		Defaults to 'default'

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	soup = BeautifulSoup(html_description, 'html.parser')

	try:
		assert soup.find(string='Approximate Measurements') != None
	except AssertionError:
		raise UnrecognizedTemplateHTML(
			'Unable to find "Approximate Measurements" string in HTML description',
			html_string=str(soup))
	else:
		data = (
			soup
			.find(string='Approximate Measurements')  # string itself
			.parent  # enclosing <h3>
			.parent  # enclosing <td>
			.parent  # enclosing <tr>
			.parent  # enclosing <tbody>
			.parent  # enclosing <table>
		)

	m_list = []

	if parse_strategy == 'default':
		strings = list(data.stripped_strings)
		try:
			m_list.append(Msmt('jacket', 'chest_flat', str2int(strings[2])))
			m_list.append(Msmt('jacket', 'sleeve', str2int(strings[4])))
			m_list.append(Msmt('jacket', 'shoulders', str2int(strings[6])))
			m_list.append(Msmt('jacket', 'waist_flat', str2int(strings[8])))
			m_list.append(Msmt('jacket', 'length', str2int(strings[10])))
			# TypeError raised by Measurement class if passed non int value
			# as the measurement value
		except TypeError as e:
			raise UnrecognizedMeasurement(
				'Instantiation of Measurement class ({}) by parsing html raised a KeyError, \
				indicating the parser identified a region that it expected would be a \
				measurement value.'.format(e), html_string=str(data))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(data),
		measurements_list=m_list)

	return m


def get_suit_measurements(html_description, parse_strategy='default'):
	"""Parses a sportcoat listing from seller balearic1 and returns the measurements
	as a dict.

	Parameters
	----------
	html_description : str
	parse_strategy : str
		Defaults to 'default'

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	soup = BeautifulSoup(html_description, 'html.parser')

	try:
		assert soup.find(string='Approximate Measurements') != None
	except AssertionError:
		raise UnrecognizedTemplateHTML(
			'Unable to find "Approximate Measurements" string in HTML description',
			html_string=str(soup))
	else:
		data = (
			soup
			.find(string='Approximate Measurements')  # string itself
			.parent  # enclosing <h3>
			.parent  # enclosing <td>
			.parent  # enclosing <tr>
			.parent  # enclosing <tbody>
			.parent  # enclosing <table>
		)

	m_list = []

	if parse_strategy == 'default':
		strings = list(data.stripped_strings)
		try:
			# Suit listings are a composite type of both sportcoat and pant types
			m_list.append(Msmt('jacket', 'chest_flat', str2int(strings[2])))
			m_list.append(Msmt('jacket', 'sleeve', str2int(strings[4])))
			m_list.append(Msmt('jacket', 'shoulders', str2int(strings[6])))
			m_list.append(Msmt('jacket', 'waist_flat', str2int(strings[8])))
			m_list.append(Msmt('jacket', 'length', str2int(strings[10])))
			m_list.append(Msmt('pant', 'waist_flat', str2int(strings[13])))
			m_list.append(Msmt('pant', 'hips_flat', str2int(strings[15])))
			m_list.append(Msmt('pant', 'inseam', str2int(strings[17])))
			m_list.append(Msmt('pant', 'cuff_height', str2int(strings[19])))
			m_list.append(Msmt('pant', 'cuff_width', str2int(strings[23])))
			m_list.append(Msmt('pant', 'rise', str2int(strings[25])))
			# TypeError raised by Measurement class if passed non int value
			# as the measurement value
		except TypeError as e:
			raise UnrecognizedMeasurement(
				'Instantiation of Measurement class ({}) by parsing html raised a KeyError, \
				indicating the parser identified a region that it expected would be a \
				measurement value.'.format(e), html_string=str(data))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'Default parsing strategy expected a differing number of measurements than \
				what was provided by the template.',
				html_string=str(data))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(data),
		measurements_list=m_list)

	return m


def get_pant_measurements(html_description, parse_strategy='default'):
	"""Parses a pants listing from seller balearic1 and returns the measurements
	as a dict.

	Parameters
	----------
	html_description : str
	parse_strategy : str
		Defaults to 'default'

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	soup = BeautifulSoup(html_description, 'html.parser')

	try:
		assert soup.find(string='Approximate Measurements') != None
	except AssertionError:
		raise UnrecognizedTemplateHTML(
			'Unable to find "Approximate Measurements" string in HTML description',
			html_string=str(soup))
	else:
		data = (
			soup
			.find(string='Approximate Measurements')  # string itself
			.parent  # enclosing <h3>
			.parent  # enclosing <td>
			.parent  # enclosing <tr>
			.parent  # enclosing <tbody>
			.parent  # enclosing <table>
		)

	m_list = []

	if parse_strategy == 'default':
		strings = list(data.stripped_strings)
		try:
			m_list.append(Msmt('pant', 'waist_flat', str2int(strings[2])))
			m_list.append(Msmt('pant', 'hips_flat', str2int(strings[4])))
			m_list.append(Msmt('pant', 'inseam', str2int(strings[6])))
			m_list.append(Msmt('pant', 'cuff_height', str2int(strings[8])))
			m_list.append(Msmt('pant', 'cuff_width', str2int(strings[12])))
			m_list.append(Msmt('pant', 'rise', str2int(strings[14])))
			# TypeError raised by Measurement class if passed non int value
			# as the measurement value
		except TypeError as e:
			raise UnrecognizedMeasurement(
				'Instantiation of Measurement class ({}) by parsing html raised a KeyError, \
				indicating the parser identified a region that it expected would be a \
				measurement value.'.format(e), html_string=str(data))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'Default parsing strategy expected a differing number of measurements than \
				what was provided by the template.',
				html_string=str(data))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(data),
		measurements_list=m_list)

	return m


def get_casual_shirt_measurement(html_description, parse_strategy='default'):
	"""Parses a casual shirt listing from seller balearic1 and returns a
	MeasurementsCollection instance.

	This parsing function cannot provide qualitative diffrentiation between short and
	long sleeve shirts.

	Parameters
	----------
	html_description : str
	parse_strategy : str
		Defaults to 'default'

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	soup = BeautifulSoup(html_description, 'html.parser')

	try:
		assert soup.find(string='Approximate Measurements') != None
	except AssertionError:
		raise UnrecognizedTemplateHTML(
			'Unable to find "Approximate Measurements" string in HTML description',
			html_string=str(soup))
	else:
		data = (
			soup
			.find(string='Approximate Measurements')  # string itself
			.parent  # enclosing <h3>
			.parent  # enclosing <td>
			.parent  # enclosing <tr>
			.parent  # enclosing <tbody>
			.parent  # enclosing <table>
		)

	m_list = []

	if parse_strategy == 'default':
		strings = list(data.stripped_strings)
		try:
			m_list.append(Msmt('shirt', 'chest_flat', str2int(strings[2])))
			m_list.append(Msmt('shirt', 'shoulders', str2int(strings[6])))
			sleeve_length = str2int(strings[4])
			if sleeve_length >= 18000:
				m_list.append(Msmt('shirt', 'sleeve_long', sleeve_length))
			elif sleeve_length <= 13000:
				m_list.append(Msmt('shirt', 'sleeve_short', sleeve_length))
			else:
				raise UnrecognizedMeasurement(
					'Expected sleeve length to be <= 13000 or >= 18000. \
					Received: <{}>'.format(sleeve_length), html_string=str(data))
			# TypeError raised by Measurement class if passed non int value
			# as the measurement value
		except TypeError as e:
			raise UnrecognizedMeasurement(
				'Instantiation of Measurement class ({}) by parsing html raised a KeyError, \
				indicating the parser identified a region that it expected would be a \
				measurement value.'.format(e), html_string=str(data))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'Default parsing strategy expected a differing number of measurements than \
				what was provided by the template.',
				html_string=str(data))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(data),
		measurements_list=m_list)

	return m


def get_dress_shirt_measurement(html_description, parse_strategy='default'):
	"""Parses a dress shirt listing from seller balearic1 and returns a
	MeasurementsCollection instance.

	This parsing function cannot provide qualitative diffrentiation between short and
	long sleeve shirts.

	Parameters
	----------
	html_description : str
	parse_strategy : str
		Defaults to 'default'

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	soup = BeautifulSoup(html_description, 'html.parser')

	try:
		assert soup.find(string='Approximate Measurements') != None
	except AssertionError:
		raise UnrecognizedTemplateHTML(
			'Unable to find "Approximate Measurements" string in HTML description',
			html_string=str(soup))
	else:
		data = (
			soup
			.find(string='Approximate Measurements')  # string itself
			.parent  # enclosing <h3>
			.parent  # enclosing <td>
			.parent  # enclosing <tr>
			.parent  # enclosing <tbody>
			.parent  # enclosing <table>
		)

	m_list = []

	if parse_strategy == 'default':
		strings = list(data.stripped_strings)
		try:
			m_list.append(Msmt('shirt', 'chest_flat', str2int(strings[2])))
			m_list.append(Msmt('shirt', 'shoulders', str2int(strings[6])))
			sleeve_length = str2int(strings[4])
			if sleeve_length >= 18000:
				m_list.append(Msmt('shirt', 'sleeve_long', sleeve_length))
			elif sleeve_length <= 13000:
				m_list.append(Msmt('shirt', 'sleeve_short', sleeve_length))
			else:
				raise UnrecognizedMeasurement(
					'Expected sleeve length to be <= 13000 or >= 18000. \
					Received: <{}>'.format(sleeve_length), html_string=str(data))
			# TypeError raised by Measurement class if passed non int value
			# as the measurement value
		except TypeError as e:
			raise UnrecognizedMeasurement(
				'Instantiation of Measurement class ({}) by parsing html raised a KeyError, \
				indicating the parser identified a region that it expected would be a \
				measurement value.'.format(e), html_string=str(data))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'Default parsing strategy expected a differing number of measurements than \
				what was provided by the template.',
				html_string=str(data))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(data),
		measurements_list=m_list)

	return m


def get_coat_and_jacket_measurements(html_description, parse_strategy='default'):
	"""Parses a coat/jacket listing from seller balearic1 and returns a
	MeasurementsCollection instance.

	Parameters
	----------
	html_description : str
	parse_strategy : str
		Defaults to 'default'

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	logger.debug('Beginning coats&jackets parser')

	soup = BeautifulSoup(html_description, 'html.parser')

	try:
		assert soup.find(string='Approximate Measurements') != None
	except AssertionError:
		raise UnrecognizedTemplateHTML(
			'Unable to find "Approximate Measurements" string in HTML description',
			html_string=str(soup))
	else:
		data = (
			soup
			.find(string='Approximate Measurements')  # string itself
			.parent  # enclosing <h3>
			.parent  # enclosing <td>
			.parent  # enclosing <tr>
			.parent  # enclosing <tbody>
			.parent  # enclosing <table>
		)

	m_list = []

	logger.debug('Using <%s> parsing strategy' % parse_strategy)

	if parse_strategy == 'default':
		strings = list(data.stripped_strings)
		try:
			m_list.append(Msmt('jacket', 'chest_flat', str2int(strings[2])))
			m_list.append(Msmt('jacket', 'sleeve', str2int(strings[4])))
			m_list.append(Msmt('jacket', 'shoulders', str2int(strings[6])))
			m_list.append(Msmt('jacket', 'length', str2int(strings[8])))
			# TypeError raised by Measurement class if passed non int value
			# as the measurement value
		except TypeError as e:
			raise UnrecognizedMeasurement(
				'Instantiation of Measurement class ({}) by parsing html raised a KeyError, \
				indicating the parser identified a region that it expected would be a \
				measurement value.'.format(e), html_string=str(data))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'Default parsing strategy expected a differing number of measurements than \
				what was provided by the template.',
				html_string=str(data))
	elif parse_strategy == 'new_v1':

		search_for = [
			PP(attribute='sleeve', pattern=re.compile('sleeve', re.IGNORECASE)),
			PP(attribute='chest_flat', pattern=re.compile('pit to pit', re.IGNORECASE)),
			PP(attribute='shoulders', pattern=re.compile('shoulder seams', re.IGNORECASE)),
			PP(attribute='length', pattern=re.compile('length', re.IGNORECASE)),
			PP(attribute='waist_flat', pattern=re.compile('waist', re.IGNORECASE), required=False)]

		for pp in search_for:
			pp.category = 'jacket'

		for parse_param in search_for:
			logger.debug(
				'Searching template for %s, using pattern <%r>' % (
					parse_param.attribute, parse_param.pattern))

			# Find search phrase in soup
			navigable_str = data.find(string=parse_param.pattern)
			if navigable_str is None:
				if parse_param.required:
					logger.warn(
						'get_coat_and_jacket_measurements method did not find a match for pattern: <%r> in the template HTML.' % parse_param.pattern)
					raise UnrecognizedTemplateHTML(
						'Parser did not find an expected regex pattern: <{}> in template HTML'
						.format(repr(parse_param.pattern)),
						html_string=str(data))
				else:
					logger.debug('Did not find match')
			else:
				# Find measurement value paired to search phrase
				msmt = navigable_str.find_parent('td').find_next_sibling('td').string

				if msmt is None:
					debug.warn('get_coat_and_jacket_measurements method could not find a sibling measurement for <%r>' % navigable_str)
					raise UnrecognizedTemplateHTML(
						'Parser could not find accompanying measurement value for <%r>'.format(navigable_str),
						html_string=str(data))
				else:
					# Convert it from text decimal to integer and add to the list
					m = Msmt(parse_param.category, parse_param.attribute, str2int(msmt))
					logger.debug('Parsed out and built Measurement: <%r>' % m)
					m_list.append(m)


		"""should_have = [
			('sleeve', 'sleeve'),
			('pit to pit', 'chest_flat'),
			('shoulder', 'shoulders'),
			('length', 'length')]

		could_have = [
			('waist', 'waist_flat')]

		for search_phrase, msmt_type in should_have:
			logger.debug('Searching template for <%r>' % search_phrase)

			# Find search phrase in soup
			navigable_str = data.find(string=re.compile(search_phrase, re.IGNORECASE))

			if navigable_str is None:
				logger.warn(
					'get_coat_and_jacket_measurements method did not find an expected string: <%r> in the template HTML.' % navigable_str)
				raise UnrecognizedTemplateHTML(
					'Parser did not find an expected string: <{}> in template HTML'
					.format(navigable_str),
					html_string=str(data))
			else:
				# Find measurement value paired to search phrase
				msmt = navigable_str.find_parent('td').find_next_sibling('td').string
				if msmt is None:
					logger.warn(
						'get_coat_and_jacket_measurements method did not find paired meaasurement for: <%r> in the template HTML.' % navigable_str)
					raise UnrecognizedMeasurement(
						'Search for a measurement value paired to the string <{}> failed.'.format(search_phrase))

				# Convert it from text decimal to integer and add to the list
				m = Msmt('jacket', msmt_type, str2int(msmt))
				logger.debug('Parsed out and built Measurement: %r' % m)
				m_list.append(m)

		# Build 'could haves' (Spoo doesn't list waist measurements for casual coats and jackets)

		for search_phrase, msmt_type in could_have:
			logger.debug('Searching template for <%r>' % search_phrase)

			# Find search phrase in soup
			navigable_str = data.find(string=re.compile(search_phrase, re.IGNORECASE))

			if navigable_str is None:
				logger.debug(
					'get_coat_and_jacket_measurements method did not find string: <%r> in the template HTML.' % navigable_str)
			else:
				# Find measurement value paired to search phrase
				msmt = navigable_str.find_parent('td').find_next_sibling('td').string
				if msmt is None:
					logger.warn(
						'get_coat_and_jacket_measurements method did not find paired meaasurement for: <%r> in the template HTML.' % navigable_str)
					raise UnrecognizedMeasurement(
						'Search for a measurement value paired to the string <{}> failed.'.format(search_phrase))

				# Convert it from text decimal to integer and add to the list
				m = Msmt('jacket', msmt_type, str2int(msmt))
				logger.debug('Parsed out and built Measurement: %r' % m)
				m_list.append(m)"""


	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(data),
		measurements_list=m_list)

	return m


def get_sweater_measurements(html_description, parse_strategy='default'):
	"""Parses a sweater listing from seller balearic1 and returns a
	MeasurementsCollection instance.

	parse_strategy='default' attempts to detect raglan shoulders and sleeves
	measured from underarm and act accordingly.
	accordingly.

	Parameters
	----------
	html_description : str
	parse_strategy : str
		Defaults to 'default'

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	soup = BeautifulSoup(html_description, 'html.parser')

	try:
		assert soup.find(string='Approximate Measurements') != None
	except AssertionError:
		raise UnrecognizedTemplateHTML(
			'Unable to find "Approximate Measurements" string in HTML description',
			html_string=str(soup))
	else:
		data = (
			soup
			.find(string='Approximate Measurements')  # string itself
			.parent  # enclosing <h3>
			.parent  # enclosing <td>
			.parent  # enclosing <tr>
			.parent  # enclosing <tbody>
			.parent  # enclosing <table>
		)

	m_list = []

	if parse_strategy == 'default':
		sweater_uses_raglan = data.find(
			string=re.compile('raglan', flags=re.IGNORECASE)) is not None
		sweater_uses_underarm = data.find(
			string=re.compile('underarm', flags=re.IGNORECASE)) is not None

		if sweater_uses_raglan != sweater_uses_underarm:
			raise UnrecognizedTemplateHTML(
				'Expected template text search for "raglan" and "underarm" to BOTH == True\
				or BOTH == False. Found raglan={} and sweater_uses_underarm={}'.format(
					sweater_uses_raglan, sweater_uses_underarm), html_string=str(data))

		strings = list(data.stripped_strings)
		try:
			m_list.append(Msmt('sweater', 'chest_flat', str2int(strings[2])))
			m_list.append(Msmt('sweater', 'length', str2int(strings[8])))

			# Handle cases with raglan sleeves or not
			if sweater_uses_raglan and sweater_uses_underarm:
				m_list.append(Msmt('sweater', 'sleeve_from_armpit', str2int(strings[4])))
				m_list.append(Msmt('sweater', 'shoulders_raglan', 0))
			else:
				m_list.append(Msmt('sweater', 'sleeve', str2int(strings[4])))
				m_list.append(Msmt('sweater', 'shoulders', str2int(strings[6])))
			# TypeError raised by Measurement class if passed non int value
			# as the measurement value
		except TypeError as e:
			raise UnrecognizedMeasurement(
				'Instantiation of Measurement class ({}) by parsing html raised a KeyError, \
				indicating the parser identified a region that it expected would be a \
				measurement value.'.format(e), html_string=str(data))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'Default parsing strategy expected a differing number of measurements than \
				what was provided by the template.',
				html_string=str(data))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(data),
		measurements_list=m_list)

	return m


'''def get_suit_measurements2(html_description, parse_strategy='default'):
	"""Parses a sportcoat listing from seller balearic1 and returns the measurements
	as a dict.

	Parameters
	----------
	html_description : str
	parse_strategy : str
		Defaults to 'default'

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

	if parse_strategy == 'default':
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
			'Width of hem opening',
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
		if len(possible_pairs['Width of hem opening']) > 0:
			m_dict['pant_leg_opening'] = possible_pairs['Width of hem opening'][0]
		elif len(possible_pairs['At cuff']) > 0:
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


	return m_dict'''


function_directory = {
	3002: get_sportcoat_measurements,
	3001: get_suit_measurements,
	57991: get_dress_shirt_measurement,
	57990: get_casual_shirt_measurement,
	57989: get_pant_measurements,
	57988: get_coat_and_jacket_measurements,
	11484: get_sweater_measurements
}








