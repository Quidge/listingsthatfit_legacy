from app.template_parsing.clothing_category_names import name_mapping as official_names

# These are the clothing categories that this parser supports.

supported_category_names = {
	'SPORTCOAT': official_names['SPORTCOAT'],
	'SUIT': official_names['SUIT'],
	'DRESS_SHIRT': official_names['DRESS_SHIRT'],
	'CASUAL_SHIRT': official_names['CASUAL_SHIRT'],
	'PANT': official_names['PANT'],
	'COAT_OR_JACKET': official_names['COAT_OR_JACKET'],
	'SWEATER': official_names['SWEATER'],
	'JEAN': official_names['JEAN']
}