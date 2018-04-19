from decimal import Decimal, getcontext

'''
for name, values_list in user_sizes_dict:
	db_set = set(values_list)
	form_set = set(form_fields[name])

	remove = db_set - form_set
	add = form_set - db_set
'''

'''
vals = [3225, 3200, 3250]
for val in vals:
	getcontext().prec = 4
	dec = Decimal(val)
	new_val = format(dec/Decimal(100), '.2f') 
	print(val, dec, new_val)
	print('val type: ', type(val))
	print('dec type: ', type(dec))
	print('new_val type: ', type(new_val))
'''

dec = 32.50

print(dec, type(dec), int(dec*100))