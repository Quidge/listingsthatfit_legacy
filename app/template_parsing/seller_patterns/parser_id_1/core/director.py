import logging
import re
from bs4 import BeautifulSoup
from app.template_parsing.exception import (
	UnrecognizedMeasurement,
	UnsupportedParsingStrategy,
	UnsupportedClothingCategory,
	UnrecognizedTemplateHTML)
from app.template_parsing import Measurement as Msmt
from app.template_parsing import MeasurementsCollection
from app.template_parsing.utils import str_measurement_to_int as str2int

logger = logging.getLogger(__name__)


def get_sportcoat_measurements(measurements_table_soup, parse_strategy='default'):
	"""Parses a sportcoat listing from seller balearic1 and returns the measurements
	as a dict.

	Parameters
	----------
	measurements_table_soup : BeautifulSoup instance
	parse_strategy='default' : str

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	logger.debug('Attempting to parse as a sportcoat')

	if type(measurements_table_soup) is not BeautifulSoup:
		raise ValueError('Must be given a BeautifulSoup object')

	m_list = []

	if parse_strategy == 'default':
		logger.debug('Using parse_strategy={}'.format(parse_strategy))
		strings = list(measurements_table_soup.stripped_strings)
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
				measurement value.'.format(e), html_string=str(measurements_table_soup))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'parse_strategy={} expected a differing number of measurements than \
				what was provided by the template.'.format(parse_strategy),
				html_string=str(data))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(
				parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(measurements_table_soup),
		measurements_list=m_list)

	return m


def get_suit_measurements(measurements_table_soup, parse_strategy='default'):
	"""Parses a sportcoat listing from seller balearic1 and returns the measurements
	as a dict.

	Parameters
	----------
	measurements_table_soup : BeautifulSoup instance
	parse_strategy='default' : str

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	logger.debug('Attempting to parse as a suit')

	if type(measurements_table_soup) is not BeautifulSoup:
		raise ValueError('Must be given a BeautifulSoup object')

	m_list = []

	if parse_strategy == 'default':
		logger.debug('Using parse_strategy={}'.format(parse_strategy))
		strings = list(measurements_table_soup.stripped_strings)
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
				measurement value.'.format(e), html_string=str(measurements_table_soup))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'parse_strategy={} expected a differing number of measurements than \
				what was provided by the template.'.format(parse_strategy),
				html_string=str(measurements_table_soup))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(
				parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(measurements_table_soup),
		measurements_list=m_list)

	return m


def get_pant_measurements(measurements_table_soup, parse_strategy='default'):
	"""Parses a pants listing from seller balearic1 and returns the measurements
	as a dict.

	Parameters
	----------
	measurements_table_soup : BeautifulSoup instance
	parse_strategy='default' : str

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	logger.debug('Attempting to parse as a pant')

	if type(measurements_table_soup) is not BeautifulSoup:
		raise ValueError('Must be given a BeautifulSoup object')

	m_list = []

	if parse_strategy == 'default':
		logger.debug('Using parse_strategy={}'.format(parse_strategy))
		strings = list(measurements_table_soup.stripped_strings)
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
				measurement value.'.format(e), html_string=str(measurements_table_soup))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'parse_strategy={} expected a differing number of measurements than \
				what was provided by the template.'.format(parse_strategy),
				html_string=str(measurements_table_soup))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(
				parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(measurements_table_soup),
		measurements_list=m_list)

	return m


def get_casual_shirt_measurements(measurements_table_soup, parse_strategy='default'):
	"""Parses a casual shirt listing from seller balearic1 and returns a
	MeasurementsCollection instance.

	This parsing function cannot provide qualitative diffrentiation between short and
	long sleeve shirts.

	Parameters
	----------
	measurements_table_soup : BeautifulSoup instance
	parse_strategy='default' : str

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	logger.debug('Attempting to parse as a casual_shirt')

	if type(measurements_table_soup) is not BeautifulSoup:
		raise ValueError('Must be given a BeautifulSoup object')

	m_list = []

	if parse_strategy == 'default':
		logger.debug('Using parse_strategy={}'.format(parse_strategy))
		strings = list(measurements_table_soup.stripped_strings)
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
					Received: <{}>'.format(sleeve_length),
					html_string=str(measurements_table_soup))
			# TypeError raised by Measurement class if passed non int value
			# as the measurement value
		except TypeError as e:
			raise UnrecognizedMeasurement(
				'Instantiation of Measurement class ({}) by parsing html raised a KeyError, \
				indicating the parser identified a region that it expected would be a \
				measurement value.'.format(e), html_string=str(measurements_table_soup))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'parse_strategy={} expected a differing number of measurements than \
				what was provided by the template.'.format(parse_strategy),
				html_string=str(measurements_table_soup))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(measurements_table_soup),
		measurements_list=m_list)

	return m


def get_dress_shirt_measurements(measurements_table_soup, parse_strategy='default'):
	"""Parses a dress shirt listing from seller balearic1 and returns a
	MeasurementsCollection instance.

	This parsing function cannot provide qualitative diffrentiation between short and
	long sleeve shirts.

	Parameters
	----------
	measurements_table_soup : BeautifulSoup instance
	parse_strategy='default' : str

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	logger.debug('Attempting to parse as a dress_shirt')

	if type(measurements_table_soup) is not BeautifulSoup:
		raise ValueError('Must be given a BeautifulSoup object')

	m_list = []

	if parse_strategy == 'default':
		logger.debug('Using parse_strategy={}'.format(parse_strategy))
		strings = list(measurements_table_soup.stripped_strings)
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
					Received: <{}>'.format(sleeve_length),
					html_string=str(measurements_table_soup))
			# TypeError raised by Measurement class if passed non int value
			# as the measurement value
		except TypeError as e:
			raise UnrecognizedMeasurement(
				'Instantiation of Measurement class ({}) by parsing html raised a KeyError, \
				indicating the parser identified a region that it expected would be a \
				measurement value.'.format(e), html_string=str(measurements_table_soup))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'parse_strategy={} expected a differing number of measurements than \
				what was provided by the template.'.format(parse_strategy),
				html_string=str(measurements_table_soup))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(measurements_table_soup),
		measurements_list=m_list)

	return m


def get_coat_and_jacket_measurements(measurements_table_soup, parse_strategy='default'):
	"""Parses a coat/jacket listing from seller balearic1 and returns a
	MeasurementsCollection instance.

	Parameters
	----------
	measurements_table_soup : BeautifulSoup instance
	parse_strategy='default' : str

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	logger.debug('Attempting to parse as a coat_or_jacket')

	if type(measurements_table_soup) is not BeautifulSoup:
		raise ValueError('Must be given a BeautifulSoup object')

	m_list = []

	if parse_strategy == 'default':
		logger.debug('Using parse_strategy={}'.format(parse_strategy))
		strings = list(measurements_table_soup.stripped_strings)
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
				measurement value.'.format(e), html_string=str(measurements_table_soup))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'parse_strategy={} expected a differing number of measurements than \
				what was provided by the template.'.format(parse_strategy),
				html_string=str(measurements_table_soup))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(measurements_table_soup),
		measurements_list=m_list)

	return m


def get_sweater_measurements(measurements_table_soup, parse_strategy='default'):
	"""Parses a sweater listing from seller balearic1 and returns a
	MeasurementsCollection instance.

	parse_strategy='default' attempts to detect raglan shoulders and sleeves
	measured from underarm and act accordingly.
	accordingly.

	Parameters
	----------
	measurements_table_soup : BeautifulSoup instance
	parse_strategy='default' : str

	Returns
	-------
	m : MeasurementsCollection instance
	"""

	logger.debug('Attempting to parse as a sweater')

	if type(measurements_table_soup) is not BeautifulSoup:
		raise ValueError('Must be given a BeautifulSoup object')

	m_list = []

	if parse_strategy == 'default':
		logger.debug('Using parse_strategy={}'.format(parse_strategy))
		strings = list(measurements_table_soup.stripped_strings)
		sweater_uses_raglan = measurements_table_soup.find(
			string=re.compile('raglan', flags=re.IGNORECASE)) is not None
		sweater_uses_underarm = measurements_table_soup.find(
			string=re.compile('underarm', flags=re.IGNORECASE)) is not None

		if sweater_uses_raglan != sweater_uses_underarm:
			raise UnrecognizedTemplateHTML(
				'Expected template text search for "raglan" and "underarm" to BOTH == True\
				or BOTH == False. Found raglan={} and sweater_uses_underarm={}'.format(
					sweater_uses_raglan, sweater_uses_underarm),
				html_string=str(measurements_table_soup))

		strings = list(measurements_table_soup.stripped_strings)
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
				measurement value.'.format(e), html_string=str(measurements_table_soup))
		except IndexError:
			raise UnrecognizedTemplateHTML(
				'parse_strategy={} expected a differing number of measurements than \
				what was provided by the template.'.format(parse_strategy),
				html_string=str(measurements_table_soup))
	else:
		raise UnsupportedParsingStrategy(
			'Parsing strategy <{}> is not supported for this category'.format(parse_strategy))
	m = MeasurementsCollection(
		parse_strategy=parse_strategy,
		parse_html=str(measurements_table_soup),
		measurements_list=m_list)

	return m


function_directory_str = {
	"sportcoat": get_sportcoat_measurements,
	"suit": get_suit_measurements,
	"dress_shirt": get_dress_shirt_measurements,
	"casual_shirt": get_casual_shirt_measurements,
	"pant": get_pant_measurements,
	"coat_or_jacket": get_coat_and_jacket_measurements,
	"sweater": get_sweater_measurements
}


def director(clothing_type):
	"""Attempts to determine which parser function to use.

	Parameters
	----------
	measurements_table_soup : BeautifulSoup object
	clothing_type_override=None : a string corresponding to one of the clothing types in the function
		directory
	ebay_primary_category_id=None : int
	ebay_secondary_category_id=None : int

	Returns
	-------
	appropriate_parse_fn : function
	"""

	logger.debug(
		'Attempting to find appropriate parsing function for clothing_type="{}"'.format(
			clothing_type))

	appropriate_parse_fn = None
	try:
		logger.debug('Attempting to find appropriate parsing function')
		appropriate_parse_fn = function_directory_str[clothing_type]
	except KeyError:
		msg = 'Parsing for <{}> is not supported'.format(clothing_type)
		logger.exception(msg)
		raise UnsupportedClothingCategory('Parsing for <{}> is not supported'.format(clothing_type))

	return appropriate_parse_fn










