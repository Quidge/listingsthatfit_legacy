import sqlalchemy as sa
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Link Tables
LinkUserSizeShirtDressSleeve = db.Table(
	'link_user_size_shirt_dress_sleeve',
	db.Column(
		'size_id',
		db.Integer,
		db.ForeignKey('size_key_shirt_dress_sleeve.id'), primary_key=True),
	db.Column(
		'user_id',
		db.Integer,
		db.ForeignKey('user.id'), primary_key=True),
	sa.UniqueConstraint('size_id', 'user_id', name='uq_association')
)

LinkUserSizeShirtDressNeck = db.Table(
	'link_user_size_shirt_dress_neck',
	db.Column(
		'size_id',
		db.Integer,
		db.ForeignKey('size_key_shirt_dress_neck.id'), primary_key=True),
	db.Column(
		'user_id',
		db.Integer,
		db.ForeignKey('user.id'), primary_key=True),
	sa.UniqueConstraint('size_id', 'user_id', name='uq_association')
)

LinkUserSizeShirtCasual = db.Table(
	'link_user_size_shirt_casual',
	db.Column(
		'size_id',
		db.Integer,
		db.ForeignKey('size_key_shirt_casual.id'), primary_key=True),
	db.Column(
		'user_id',
		db.Integer,
		db.ForeignKey('user.id'), primary_key=True),
	sa.UniqueConstraint('size_id', 'user_id', name='uq_association')
)


class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(255))

	# user many-to-many size associations (using link tables)
	sz_shirt_dress_sleeve = db.relationship(
		'SizeKeyShirtDressSleeve',
		secondary=LinkUserSizeShirtDressSleeve,
		backref=db.backref('users', lazy='dynamic'),
		order_by="asc(SizeKeyShirtDressSleeve.id)")
	sz_shirt_dress_neck = db.relationship(
		'SizeKeyShirtDressNeck',
		secondary=LinkUserSizeShirtDressNeck,
		backref=db.backref('users', lazy='dynamic'),
		order_by="asc(SizeKeyShirtDressNeck.id)")
	sz_shirt_casual = db.relationship(
		'SizeKeyShirtCasual',
		secondary=LinkUserSizeShirtCasual,
		backref=db.backref('users', lazy='dynamic'),
		order_by="asc(SizeKeyShirtCasual.id)")

	# ready for easier organization and access in JSON-esque format
	def all_sizes_in_dict(self):
		self.sizes = {
			'shirt-sleeve': {
				'key': 'shirt-sleeve',
				'relationship': self.sz_shirt_dress_sleeve
			},
			'shirt-neck': {
				'key': 'shirt-neck',
				'relationship': self.sz_shirt_dress_neck
			},
			'shirt-casual': {
				'key': 'shirt-casual',
				'relationship': self.sz_shirt_casual
			}
		}

		return self

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
		"""Returns True if user is authenticated.
		Required for Flask-login."""
		return True

	@property
	def is_active(self):
		"""True, as all users are active.
		Required for Flask-login."""
		return True

	def get_id(self):
		"""Return a user ID to satisfy Flask-login requirements."""
		return str(self.id)

	@property
	def is_anonymous(self):
		"""False. Anonymous users are not supported.
		Required for Flask-login."""
		return False

	def __repr__(self):
		return '<User id: %r, email: %r, password_hash: %r>' % (
			self.id, self.email, self.password_hash)


# Size Key Tables
class SizeKeyShirtDressSleeve(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	size = db.Column(db.Integer)

	def __repr__(self):
		return 'Dress shirt sleeve size: %r' % self.size


class SizeKeyShirtDressNeck(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	size = db.Column(db.Integer)

	def __repr__(self):
		return 'Dress shirt neck size: %r' % self.size


class SizeKeyShirtCasual(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	size_short = db.Column(db.Text(6), unique=True)
	size_long = db.Column(db.Text(20), unique=True)

	def __repr__(self):
		return 'Casual shirt size "%r" (long: "%r")' % (self.size_short, self.size_long)

