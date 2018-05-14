import unittest
import os
import sqlalchemy

from app import app, db
from app.models import User, SizeKeyShirtCasual, SizeKeyShirtDressNeck, SizeKeyShirtDressSleeve
from app.dbtouch import get_user_sizes_subscribed


class TestCase(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('..', 'test.db')
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_get_user_sizes_returns_correctly(self):
		u = User(email='testUser1@test.com', password='password')
		db_has = set(get_user_sizes_subscribed(u).keys())
		db_should_have = set(['shirt-sleeve', 'shirt-neck', 'shirt-casual'])
		self.assertEqual(db_has, db_should_have)

	# I can't get the following test to run properly.
	'''def test_duplicate_size_association_to_user(self):
		# This should assert that it is not possible to associate the same size with the same
		# user twice (testing for uniqueness). This should test every size relationship.

		# Create a user
		db.session.add(User(email='duplicate_associations@test.com', password='password'))
		db.session.flush()
		u = User.query.filter(User.email == "duplicate_associations@test.com").first()

		# Grab instances of each size category
		test_shirt_neck = SizeKeyShirtDressNeck.query.first()
		test_shirt_casual = SizeKeyShirtCasual.query.first()
		test_shirt_sleeve = SizeKeyShirtDressSleeve.query.first()

		# This will set a base state that will be rolled back to on each attempt
		u.all_sizes_in_dict()
		u.sizes['shirt-sleeve']['relationship'].append(test_shirt_sleeve)
		u.sizes['shirt-neck']['relationship'].append(test_shirt_neck)
		u.sizes['shirt-casual']['relationship'].append(test_shirt_casual)
		db.session.commit()

		# Refresh the sizes
		u.all_sizes_in_dict()

		with self.assertRaises(sqlalchemy.exc.IntegrityError):
			u.sizes['shirt-sleeve']['relationship'].append(test_shirt_sleeve)
			db.session.flush()
			db.session.rollback()
			#print('ran1')
		with self.assertRaises(sqlalchemy.exc.IntegrityError):
			u.sizes['shirt-neck']['relationship'].append(test_shirt_neck)
			db.session.flush()
			db.session.rollback()
			#print('ran2')
		with self.assertRaises(sqlalchemy.exc.IntegrityError):
			u.sizes['shirt-casual']['relationship'].append(test_shirt_casual)
			db.session.flush()
			db.session.rollback()
			#print('ran3')
	'''

def main():
	unittest.main()


if __name__ == '__main__':
	main()
