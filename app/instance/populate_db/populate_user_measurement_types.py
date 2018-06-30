from sqlalchemy.exc import IntegrityError

from app.models import UserMeasurementItemCategory, UserMeasurementItemType
from app import db

def populate_user_measurement_item_types(category):
	if category == 'suit':
		suit_types = ['']
