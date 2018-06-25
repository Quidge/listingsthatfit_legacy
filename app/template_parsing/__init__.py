# I THINK I should be organizing template_parsing as a package. Organization idea found here:
# https://docs.python.org/2/tutorial/modules.html#packages


class MeasurementsCollection(object):
	"""Base Measurements Collection class

	self.parse_strategy : str
	self.parse_html : str
		A record of the HTML string the measuremens were parsed from.
	measurement_dict : dict
	clothing_category_name : str
	"""

	def __init__(
		self, parse_strategy=None,
		parse_html=None, measurement_dict=None,
		clothing_category_name=None):

		self.parse_strategy = parse_strategy
		self.html_string = parse_html
		self.measurements = measurement_dict
		self.clothing_category_name = clothing_category_name

	def __repr__(self):
		return 'Category: {}\n{}'.format(self.clothing_category_name, self.measurements)


class Measurement(object):
	def __init__(self, category, attribute, measurement_value):
		assert type(measurement_value) == 'int'
		self.category = category
		self.attribute = attribute
		self.value = measurement_value

