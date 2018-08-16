import json

# I THINK I should be organizing template_parsing as a package. Organization idea found here:
# https://docs.python.org/2/tutorial/modules.html#packages


class ParseResult(object):
	"""An object to record the results of a parse."""

	def __init__(self, clothing_type=None, measurements=[]):
		self.clothing_type = clothing_type
		self.measurements = measurements
		self.meta = {'parse_strategy': None, 'concerns': [], 'parsed_html': None}

	def dict(self):
		return self.__dict__

	def json(self):
		return json.dumps(self.dict())

	def rehydrate(self, _json):
		"""Deserializes a json ParseResult and returns a new ParseResult instance."""
		_dict = json.loads(_json)
		new_instance = ParseResult()
		new_instance.clothing_type = _dict['clothing_type']
		new_instance.meta = _dict['meta']
		for msmt in _dict['measurements']:
			new_instance.measurements.append(
				Measurement(
					category=msmt['category'],
					attribute=msmt['attribute'],
					measurement_value=msmt['value']))
		return new_instance


class IdentifyResult(object):
	"""An object to record the results of an identification."""
	def __init__(self):
		self.html_used_to_make_observations = None
		self.ebay_primary_category_id = None
		self.ebay_secondary_category_id = None
		self.observations = {}
		self.concerns = []
		self.identified_clothing_type = None

	def dict(self):
		return self.__dict__

	def json(self):
		return json.dumps(self.dict())


class ParseParameter(object):
	"""An object holding information for the parser to look for.

	self.pattern : regex pattern
	self.alt_patterns : list of alternative regexes to use
	self._attribute : str
	self._category : str
	self.required : boolean
	"""

	def __init__(
		self, pattern, alt_patterns=[], attribute=None,
		category=None, required=True):

		self.attribute = attribute
		self.category = category
		self.pattern = pattern
		self.alt_patterns = alt_patterns
		self.required = required


class MeasurementsCollection(object):
	"""Base Measurements Collection class

	self.parse_strategy : str
	self.parse_html : str
		A record of the HTML string the measuremens were parsed from.
	measurements_list : list
		A list of Measurement class objects
	ebay_item_category_id : int
	"""

	def __init__(
		self, parse_strategy=None,
		parse_html=None, measurements_list=None,
		ebay_item_category_id=None):

		self.parse_strategy = parse_strategy
		self.html_string = parse_html
		self.measurements_list = measurements_list
		self.ebay_item_category_id = ebay_item_category_id

	def __repr__(self):
		return 'Category: {}\n{}'.format(self.ebay_item_category_id, self.measurements)


class Measurement(object):
	"""Base class for Measurement"""
	def __init__(self, category, attribute, measurement_value):
		try:
			assert type(measurement_value) == int
		except AssertionError:
			raise TypeError(
				'Measurement must be instantiated with with an int as the measurement \
				value, value given is given: <{}>'.format(measurement_value))
		self.category = category
		self.attribute = attribute
		self.value = measurement_value

	def __repr__(self):
		return '{}, {}: {}'.format(self.category, self.attribute, self.value)
