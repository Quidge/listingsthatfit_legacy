from sqlalchemy.exc import IntegrityError

from app.models import UserMeasurementItemCategory, UserMeasurementItemType
from app import db

def populate_user_measurement_item_types():
	msmt_type = [
		'sleeve',
		'chest_flat',
		'waist_flat',
		'hips_flat',
		'collar',
		'shoulders',
		'inseam',
		'outseam',
		'cuff_height',
		'cuff_width',
		'rise',
		'length'
	]

	for t in msmt_type:
		m = UserMeasurementItemType(type_name=t)
		try:
			db.session.add(m)
			db.session.flush()
		except IntegrityError:
			print('Already present: %r' % (m,))
		else:
			print('Added and flushed %r' % (m,))
	db.session.commit()

if __name__ == '__main__':
	populate_user_measurement_item_types()
