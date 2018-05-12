import unittest
import os

from app import app, db
from app.models import User
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

	def test_duplicate_size_association_to_user(self):
		# This should assert that it is not possible to associate a size with a user
		# twice. This should test every size table.
		pass


def main():
	unittest.main()


if __name__ == '__main__':
	main()
