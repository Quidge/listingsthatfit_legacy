from sqlalchemy.exc import IntegrityError

from app.models import MeasurementType
from app import db


def build_sportcoat_types():
	attrs = ['chest', 'sleeve', 'shoulders', 'waist', 'boc']
	m_types = [MeasurementType(attribute=attr, clothing_category='sportcoat') for attr in attrs]
	db.session.add_all(m_types)
	try:
		db.session.commit()
	except IntegrityError as e:
		db.session.rollback()
		raise e

	print('Success.')
	for item in m_types:
		print('Added: {}'. format(repr(item)))
