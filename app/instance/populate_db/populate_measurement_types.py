from sqlalchemy.exc import IntegrityError

from app.models import MeasurementItemType
from app import db


def build_measurement_item_types():
	m_types = [
		'chest_flat',
		'sleeve',
		'shoulders',
		'waist_flat',
		'length',
		'hips_flat',
		'inseam',
		'cuff_height',
		'cuff_width',
		'rise']

	for t in m_types:
		model = MeasurementItemType(type_name=t)
		db.session.add(model)
		try:
			db.session.commit()
		except IntegrityError:
			print(
				'Committing the following MeasurementItemType raised an integrity error. \
				Skipping and resuming.\n{}'.format(
					model))
		else:
			print('Added: {}'.format(model))


if __name__ == '__main__':
	build_measurement_item_types()








