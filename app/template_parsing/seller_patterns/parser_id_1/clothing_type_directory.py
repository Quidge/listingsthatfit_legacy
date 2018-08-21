from app.template_parsing.clothing_type_names import name_mapping as official_names

# This parser supports only these categories.

supported_category_names = {
	'SPORTCOAT': official_names['SPORTCOAT'],
	'SUIT': official_names['SUIT'],
	'DRESS_SHIRT': official_names['DRESS_SHIRT'],
	'CASUAL_SHIRT': official_names['CASUAL_SHIRT'],
	'PANT': official_names['PANT'],
	'COAT_OR_JACKET': official_names['COAT_OR_JACKET'],
	'SWEATER': official_names['SWEATER']
}