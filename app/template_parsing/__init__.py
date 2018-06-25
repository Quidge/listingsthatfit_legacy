# I THINK I should be organizing template_parsing as a package. Organization idea found here:
# https://docs.python.org/2/tutorial/modules.html#packages


class MeasurementsCollection(object):
	"""Base Measurements Collection class

	self.parse_strategy : str
	self.parse_html : str
		A record of the HTML string the measuremens were parsed from.
	measurements_list : list
		A list of Measurement class objects
	clothing_category_name : str
	"""

	def __init__(
		self, parse_strategy=None,
		parse_html=None, measurements_list=None,
		clothing_category_name=None):

		self.parse_strategy = parse_strategy
		self.html_string = parse_html
		self.measurements_list = measurements_list
		self.clothing_category_name = clothing_category_name

	def __repr__(self):
		return 'Category: {}\n{}'.format(self.clothing_category_name, self.measurements)


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

