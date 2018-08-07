import re
import logging
from bs4 import BeautifulSoup
from app.template_parsing import IdentifyResult

logger = logging.getLogger(__name__)


def identify_clothing_type(
	measurements_table_soup,
	ebay_primary_category_id=None,
	ebay_secondary_category_id=None):
	"""Attempts to identify the type of clothing.

	Parameters
	----------
	measurements_table_soup : BeautifulSoup object
	ebay_primary_category_id : int
	ebay_secondary_category_id : int

	Returns
	-------
	clothing type : str
		'dress_shirt', 'suit', 'pant', etc
	"""

	if type(measurements_table_soup) is not BeautifulSoup:
		raise TypeError(
			'measurements_table_soup parameter must be a BeautifulSoup object')

	identify_result = IdentifyResult()

	identify_result.ebay_primary_category_id = ebay_primary_category_id
	identify_result.ebay_secondary_category_id = ebay_secondary_category_id

	soup = measurements_table_soup
	identify_result.html_used_to_make_observations = str(soup)

	# identifying observations
	has_pants_section_declaration = bool(soup.find(string=re.compile('pants', re.IGNORECASE)))
	mentions_cuff = bool(soup.find(string=re.compile('cuff', re.IGNORECASE)))
	num_waist_mentions = len(soup.find_all(string=re.compile('waist', re.IGNORECASE)))
	mentions_sleeve = bool(soup.find(string=re.compile('sleeve', re.IGNORECASE)))
	mentions_length = bool(soup.find(string=re.compile('length', re.IGNORECASE)))

	identify_result.observations = {
		"pants_section_declaration": {
			"type": "proposition",
			"msg": "Listing has pants section declaration",
			"result": has_pants_section_declaration},
		"mentions_cuff": {
			"type": "proposition",
			"msg": "Listing mentions cuff",
			"result": mentions_cuff},
		"waist_mentions": {
			"type": "information",
			"msg": "Number of waist mentions",
			"result": num_waist_mentions},
		"mentions_sleeve": {
			"type": "proposition",
			"msg": "Listing mentions sleeve",
			"result": mentions_sleeve},
		"mentions_length": {
			"type": "proposition",
			"msg": "Listing mentions length",
			'result': mentions_length},
	}

	if has_pants_section_declaration:
		# Should be a suit. Spoo's listings ONLY have 'pants' in suit listings
		logger.debug('Identify thinks this template belongs to a suit listing.')
		if num_waist_mentions is not 2:
			msg = (
				'Identify expected suit template to match CA "waist" twice, got: '
				'num_waist_mentions={}').format(num_waist_mentions)
			identify_result.concerns.append(msg)
			logger.warn(msg)
		if not mentions_cuff:
			msg = 'Identify expected suit template to match CA "cuff". It didnt'
			identify_result.concerns.append(msg)
			logger.warn(msg)
		if ebay_primary_category_id and ebay_primary_category_id != 3001:
			msg = (
				'Identify expected primary category to be 3001. '
				'Instead ebay_primary_category_id={}').format(ebay_primary_category_id)
			identify_result.concerns.append(msg)
			logger.warn(msg)

		identify_result.identified_clothing_type = 'suit'

	elif mentions_cuff and not mentions_sleeve:
		# Should be a pant listing.
		logger.debug('Identify thinks this template belongs to a pant listing.')
		if num_waist_mentions is not 1:
			msg = (
				'Identify expected pant template to match CA "waist" twice, '
				'got: num_waist_mentions={}').format(num_waist_mentions)
			identify_result.concerns.append(msg)
			logger.warn(msg)
		if ebay_primary_category_id and ebay_primary_category_id != 57989:
			msg = (
				'Identify expected primary category to be 57989. Instead '
				'ebay_primary_category_id={}').format(ebay_primary_category_id)
			identify_result.concerns.append(msg)
			logger.warn(msg)

		identify_result.identified_clothing_type = 'pant'

	elif mentions_sleeve and not mentions_length:
		# Should be either dress shirt or casual shirt. These have the same measurement descriptions so
		# diffrentiating requires the item category.
		if ebay_primary_category_id == 57991:
			identify_result.identified_clothing_type = 'dress_shirt'
			logger.debug('Identify thinks this template belongs to a dress shirt listing.')

		elif ebay_primary_category_id == 57990:
			identify_result.identified_clothing_type = 'casual_shirt'
			logger.debug('Identify thinks this template belongs to a casual shirt listing.')

		elif ebay_primary_category_id is None:
			msg = (
				'Identify received ebay_primary_category_id=None for a listing '
				'it thinks is a dress or casual shirt. Without this there is no way '
				'to discern. Defaulting to casual_shirt.')
			identify_result.identified_clothing_type = 'casual_shirt'
			identify_result.concerns.append(msg)
			logger.warn(msg)
		else:
			msg = (
				'Identify received ebay_primary_category_id={} for a listing it '
				'thinks is a dress or casual shirt (57991 or 57990). Without this '
				'there is no way to discern. Defaulting to casual_shirt.').format(
					ebay_primary_category_id)
			identify_result.identified_clothing_type = 'casual_shirt'
			identify_result.concerns.append(msg)
			logger.warn(msg)

	elif mentions_sleeve and mentions_length and num_waist_mentions == 0:
		# Either sweater or casual jacket. Sportcoats will have waist mentions.
		if ebay_primary_category_id == 11484:
			logger.debug('Identify thinks this template belongs to a sweater listing.')
			identify_result.identified_clothing_type = 'sweater'

		elif ebay_primary_category_id == 57988:
			logger.debug('Identify thinks this template belongs to a coat_or_jacket listing.')
			identify_result.identified_clothing_type = 'coat_or_jacket'

		elif ebay_primary_category_id == 3001:
			msg = (
				'Identify thinks this template belongs to a coat_or_jacket listing, '
				'but expected ebay_primary_category_id=57988. Instead received '
				'ebay_primary_category_id=3001')
			logger.warn(msg)
			identify_result.identified_clothing_type = 'coat_or_jacket'
			identify_result.concerns.append(msg)

		elif not ebay_primary_category_id:
			msg = (
				'Identify received ebay_primary_category_id=None for a listing it '
				'thinks is a sweater or casual jacket. Without this there is no way '
				'to discern. This is significant enough that Identify will return '
				'None and the parser will probably fail for this listing.')
			logger.warn(msg)
			identify_result.concerns.append(msg)
			identify_result.identified_clothing_type = None

		else:
			msg = (
				'Identify received ebay_primary_category_id={} for a listing it '
				'thinks is a sweater or coat_or_jacket. This is significant enough '
				'that Identify will return None and the parser will probably fail for '
				'this listing.').format(ebay_primary_category_id)
			logger.warn(msg)
			identify_result.concerns.append(msg)
			identify_result.identified_clothing_type = None

	elif num_waist_mentions == 1 and not mentions_cuff:
		# Should be a sportcoat
		logger.debug('Identify thinks this template belongs to a sportcoat listing.')
		if ebay_primary_category_id != 57988 or ebay_primary_category_id != 57988:
			msg = (
				'Idenfity received ebay_primary_category_id={} and expected'
				'ebay_primary_category_id=3001 or ebay_primary_category_id=57988 '
				'(deprecated). This is significant enough that Identify will return '
				'None and the parser will probably fail for this listing.').format(
					ebay_primary_category_id)
			logger.warn(msg)
			identify_result.concerns.append(msg)
			identify_result.identified_clothing_type = None

		elif ebay_primary_category_id == 57988:
			msg = (
				'Identify thinks this template belongs to a sportcoat listing, but '
				'expected ebay_primary_category_id=3001. Instead received '
				'ebay_primary_category_id=57988. Spoo has said that this should be '
				'deprecated and sportcoats should be only listed in 3001.')
			logger.warn(msg)
			identify_result.concerns.append(msg)
			identify_result.identified_clothing_type = 'sportcoat'

	else:
		msg = 'Identify failed to indentify the listing.'
		logger.warn(msg)
		identify_result.concerns.append(msg)
		identify_result.identified_clothing_type = None

	return identify_result
