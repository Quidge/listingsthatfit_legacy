from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(255))

	@property
	def password(self):
		raise AttributeError('password is read only')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	@property
	def is_authenticated(self):
		"""Returns True if user is authenticated."""
		return True

	@property
	def is_active(self):
		"""True, as all users are active."""
		return True

	def get_id(self):
		"""Return a user ID to satisfy Flask-login requirements."""
		return str(self.id)

	@property
	def is_anonymous(self):
		"""False. Anonymous users are not supported."""
		return False

	def __repr__(self):
		return '<User id: %r, email: %r, password: %r>' % (self.id, self.email, self.password)

# Size Key Tables
class SizeKeyShirtDressSleeve(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	size = db.Column(db.Numeric(4,2))

	def __repr__(self):
		return 'Dress shirt sleeve size: %r' % self.size

class SizeKeyShirtDressNeck(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	size = db.Column(db.Numeric(4,2))

	def __repr__(self):
		return 'Dress shirt neck size: %r' % self.size

class SizeKeyShirtCasual(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	size_short = db.Column(db.Text(6), unique=True)
	size_long = db.Column(db.Text(20), unique=True)

	def __repr__(self):
		return 'Casual shirt size "%r" (long: "%r")' % (self.size_short, self.size_long)

# Link Tables
LinkUserSizeShirtDressSleeve = db.Table(
	'link_user_size_shirt_dress_sleeve',
	db.Column('size_id', db.Integer, db.ForeignKey('size_key_shirt_dress_sleeve.id'), primary_key=True),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

LinkUserSizeShirtDressNeck = db.Table(
	'link_user_size_shirt_dress_neck',
	db.Column('size_id', db.Integer, db.ForeignKey('size_key_shirt_dress_neck.id'), primary_key=True),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

LinkUserSizeShirtCasual = db.Table(
	'link_user_size_shirt_casual',
	db.Column('size_id', db.Integer, db.ForeignKey('size_key_shirt_casual.id'), primary_key=True),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

