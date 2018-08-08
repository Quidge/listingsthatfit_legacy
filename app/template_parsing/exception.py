class TemplateParsingError(Exception):
	"""Base class for exceptions in template_parsing module"""
	pass


class UnsupportedParsingStrategy(TemplateParsingError):
	"""Exception raised when parsing strategy is not supported"""
	pass


class UnsupportedClothingCategory(TemplateParsingError):
	"""Exception raised when the clothing category or type is not supported
	by the parser."""
	def __init__(
		self, message, clothing_category_id=None,
		clothing_type_name=None):
		self.message = message
		self.clothing_category_id = clothing_category_id
		self.clothing_type_name = clothing_type_name


class UnrecognizedTemplateHTML(TemplateParsingError):
	"""Base class for exceptions raised when there is a problem with the description
	HTML

	Attributes
	----------
	message : str
	html_string : str
	"""
	def __init__(self, message, html_string):
		self.message = message
		self.html_string = html_string


class UnrecognizedMeasurement(UnrecognizedTemplateHTML):
	"""Exception raised when there is trouble recognizing a measurement value."""
	pass

