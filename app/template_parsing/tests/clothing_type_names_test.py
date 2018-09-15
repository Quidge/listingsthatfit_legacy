from app.template_parsing.clothing_category_names import name_mapping


def test_name_mapping_contains_only_the_following():
	should_only_have = [
		'SPORTCOAT', 'DRESS_SHIRT', 'SUIT', 'JEAN',
		'CASUAL_SHIRT', 'PANT', 'COAT_OR_JACKET', 'SWEATER']
	assert set(name_mapping.keys()) == set(should_only_have)


def test_name_maps_to_expected():
	assert name_mapping["SPORTCOAT"] == 'sportcoat'
	assert name_mapping["SUIT"] == 'suit'
	assert name_mapping["DRESS_SHIRT"] == 'dress_shirt'
	assert name_mapping["CASUAL_SHIRT"] == 'casual_shirt'
	assert name_mapping["PANT"] == 'pant'
	assert name_mapping["COAT_OR_JACKET"] == 'coat_or_jacket'
	assert name_mapping["SWEATER"] == 'sweater'
	assert name_mapping["JEAN"] == 'jean'
