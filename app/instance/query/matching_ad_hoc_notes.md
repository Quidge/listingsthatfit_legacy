### Core problem:
###### Measurements for a clothing category (suit, sc, sweater) must be UNDERSTOOD as a block (chest + shoulder + sleeve + waist + etc), not as individual measurements (chest, shoulder, sleeve). YET, they're given and recorded most easily as individuals measurements. For example, a pants item:
```
'measurements_list': [
				('pant', 'waist_flat', 15500),
				('pant', 'hips_flat', 16000),
				('pant', 'inseam', 31000),
				('pant', 'rise', 10500)
			]
```
###### Because blocks can be on the fly constructed from individuals, these individual/block distinctions don't matter much until certain cases that require conditional logic. A sweater *will*have both a `chest` and `length` measurement, but *either* a set of `shoulders` and `sleeve` measurments **or** a set of `shoulders_raglan` and `sleeve_from_armpit` measurements.