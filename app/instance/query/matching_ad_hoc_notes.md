### Core problem:
- Measurements for a clothing category (suit, sc, sweater) must be UNDERSTOOD as a block (chest + shoulder + sleeve + waist + etc), not as individual measurements (chest, shoulder, sleeve). YET, they're given and recorded most easily as individuals measurements. For example, a pants item:
```
'measurements_list': [
				('pant', 'waist_flat', 15500),
				('pant', 'hips_flat', 16000),
				('pant', 'inseam', 31000),
				('pant', 'rise', 10500)
			]
```
- Because a block of measurements constructed from individuals easily on the fly, these individual/block distinctions don't matter much until certain cases that require conditional logic. A sweater *will* have both a `chest` and `length` measurement, but *either* a set of `shoulders` and `sleeve` measurments **or** a set of `shoulders_raglan` and `sleeve_from_armpit` measurements. At that point, it *does* matter if a sweater block with a `shoulders` measurement is missing a `sleeve` measurement.
- The problem gets bad when I'm configuring the SQL clause. "Look for sweaters with a set: sleeves between x and x, and shoulders between x and x OR a different set: sleeves_from_armpit between x and x, and shoulders_raglan between x and x." I can write that logic out, but how do I format a simple *list* of measurements that can be read also confer that conditional logic? I want to be able to record a simple set of measurements and tolerances like:
```
'measurements_list': [
			MQP('sweater', 'chest_flat', 24250, 250),
			MQP('sweater', 'shoulders', 19625, 500),
			MQP('sweater', 'shoulders_raglan', 0, 0),
			MQP('sweater', 'sleeve', 26000, 1500),
			MQP('sweater', 'sleeve_from_armpit', 19250, 2000)
		],
```

### Possible solutions
- Configure the logic at the list/input level, having something that looks like this:
```
'measurements_list': [
			MQP('sweater', 'chest_flat', 24250, 250),
			[
				MQP('sweater', 'shoulders_raglan', 0, 0)
				MQP('sweater', 'sleeve_from_armpit', 19250, 2000)
			],
			[
				MQP('sweater', 'shoulders', 19625, 500),
				MQP('sweater', 'sleeve', 26000, 1500),
			]
		],
```
In this case, the or is inferred from the sub-list.
- Configure the logic at the parser level (psuedo code):
```python
def measurement_block_query_builder(block_list_of_measurements, maybe_a_clothing_category_name?):
	"""Takes in a list of MQP parameters, and, based on ...something is able to construct a block sqlalchemy clause with _and()s and _or()s configured properly."""

	# <do_code>

	return sqlalchemy_clause
```
- Configure the logic at the list/input level, but don't interfere with the list. Have an accompanying construction schema that the parser will use to interpret the list:
```
'construction_schema': {
	and [('sweater, chest_flat')],
	or [
		and [('sweater', 'shoulders'), ('sweater', 'sleeve')],
		and [('sweater', 'shoulders_raglan'), ('sweater', 'sleeve_from_armpit')]
		]
}
'measurements_list': [
			MQP('sweater', 'chest_flat', 24250, 250),
			MQP('sweater', 'shoulders', 19625, 500),
			MQP('sweater', 'sleeve', 26000, 1500),
			MQP('sweater', 'shoulders_raglan', 0, 0),
			MQP('sweater', 'sleeve_from_armpit', 19250, 2000)
		],
```
If construction_schema is missing, default to applying every individual measurement criteria as an `and`.










