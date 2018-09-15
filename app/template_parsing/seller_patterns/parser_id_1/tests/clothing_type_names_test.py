from ..clothing_type_directory import supported_category_names


def test_supported_category_names_only_contains_the_following():
	should_only_have = [
		'SPORTCOAT', 'DRESS_SHIRT', 'SUIT', 'JEAN',
		'CASUAL_SHIRT', 'PANT', 'COAT_OR_JACKET', 'SWEATER']
	assert set(supported_category_names.keys()) == set(should_only_have)
