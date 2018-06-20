import sqlalchemy as sa
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class UniqueSet(object):
	"""
	This class behaves just like a set type collection, but will error if
	a duplicate is added to the collection.
	"""

	__emulates__ = set

	def __init__(self):
		self.data = set()

	@sa.orm.collections.collection.appender
	def append(self, item):
		"""Performs set.add(element) unless element is already present in
		the set, in which case a ValueError will be raised."""
		try:
			assert item not in self.data
		except AssertionError:
			raise ValueError('Value "{}" already exists in set'.format(item))
		else:
			self.data.add(item)

	def remove(self, item):
		self.data.remove(item)

	def __iter__(self):
		return iter(self.data)

	def __repr__(self):
		return str(self.data)


# Link Tables
LinkUserSizeShirtDressSleeve = db.Table(
	'link_user_accounts_size_shirt_dress_sleeve',
	db.Column(
		'size_id',
		db.Integer,
		db.ForeignKey('size_key_shirt_dress_sleeve.id'), primary_key=True),
	db.Column(
		'user_id',
		db.Integer,
		db.ForeignKey('user_accounts.id'), primary_key=True),
	sa.UniqueConstraint('size_id', 'user_id', name='uq_association')
)

LinkUserSizeShirtDressNeck = db.Table(
	'link_user_accounts_size_shirt_dress_neck',
	db.Column(
		'size_id',
		db.Integer,
		db.ForeignKey('size_key_shirt_dress_neck.id'), primary_key=True),
	db.Column(
		'user_id',
		db.Integer,
		db.ForeignKey('user_accounts.id'), primary_key=True),
	sa.UniqueConstraint('size_id', 'user_id', name='uq_association')
)

LinkUserSizeShirtCasual = db.Table(
	'link_user_accounts_size_accounts_shirt_casual',
	db.Column(
		'size_id',
		db.Integer,
		db.ForeignKey('size_key_shirt_casual.id'), primary_key=True),
	db.Column(
		'user_id',
		db.Integer,
		db.ForeignKey('user_accounts.id'), primary_key=True),
	sa.UniqueConstraint('size_id', 'user_id', name='uq_association')
)


class EbaySeller(db.Model):
	__tablename__ = 'ebay_sellers'
	id = db.Column(db.Integer, primary_key=True)
	ebay_seller_id = db.Column(db.Text(255), unique=True)
	store_url = db.Column(db.Text(255), unique=False, nullable=True)
	all_items_url = db.Column(db.Text(255), unique=False, nullable=True)
	
	template_parser_id = db.Column(db.Integer, db.ForeignKey('template_parser.template_parser_id'))
	template_parser = db.relationship('TemplateParser', back_populates='sellers')

	items = db.relationship('Item', back_populates='seller')

	def __repr__(self):
		return '<eBay seller id: %r>' % (self.ebay_seller_id)


class TemplateParser(db.Model):
	__tablename__ = 'template_parser'
	template_parser_id = db.Column(db.Integer, primary_key=True)
	file_name_number = db.Column(db.Integer)
	parser_file_description = db.Column(sa.String(140))
	sellers = db.relationship('EbaySeller', back_populates='template_parser')

	def __repr__(self):
		return 'file_name_number: <{}> description: <"{}">'.format(self.file_name_number, self.parser_file_description)


LinkUserSubscribedSeller = db.Table(
	'link_user_accounts_subscribed_seller',
	db.Column('seller_id', db.Integer, db.ForeignKey('ebay_sellers.id')),
	db.Column('user_accounts_id', db.Integer, db.ForeignKey('user_accounts.id')),
	db.UniqueConstraint('seller_id', 'user_accounts_id', name='uq_seller_user_subscription')
)


class User(db.Model):
	__tablename__ = 'user_accounts'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(255))

	subbed_sellers = db.relationship(
		'EbaySeller',
		secondary=LinkUserSubscribedSeller,
		backref=db.backref('ebay_sellers', lazy='dynamic'),
		collection_class=lambda: UniqueSet()
	)

	# user many-to-many size associations (using link tables)
	sz_shirt_dress_sleeve = db.relationship(
		'SizeKeyShirtDressSleeve',
		secondary=LinkUserSizeShirtDressSleeve,
		backref=db.backref('users', lazy='dynamic'),
		order_by="asc(SizeKeyShirtDressSleeve.id)",
		collection_class=lambda: UniqueSet()
	)
	sz_shirt_dress_neck = db.relationship(
		'SizeKeyShirtDressNeck',
		secondary=LinkUserSizeShirtDressNeck,
		backref=db.backref('users', lazy='dynamic'),
		order_by="asc(SizeKeyShirtDressNeck.id)",
		collection_class=lambda: UniqueSet()
	)
	sz_shirt_casual = db.relationship(
		'SizeKeyShirtCasual',
		secondary=LinkUserSizeShirtCasual,
		backref=db.backref('users', lazy='dynamic'),
		order_by="asc(SizeKeyShirtCasual.id)",
		collection_class=lambda: UniqueSet()
	)

	# ready for easier organization and access in JSON-esque format
	def all_sizes_in_dict(self):
		"""Initializes self.sizes, which is a dict directory of size-key-types
		mapped to an object holding the relationship and (redundant) size-key.

		Returns
		-------
		self.sizes : dict
			self.sizes is a dict in the form:
				{
					'shirt-sleeve': {
						'key': 'shirt-sleeve',
						'relationship': self.sz_shirt_sleeve
					},
					...
				}
		"""

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

		return self.sizes

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


class ItemMeasurementAssociation(db.Model):
	__tablename__ = 'link_measurement_values_types'
	fk_measurement_id = db.Column(db.Integer, db.ForeignKey('measurement_types.id'), primary_key=True)

	# ebay_item_id is a confusing name. This refers to the items table internal id, NOT ebay's item id.
	fk_ebay_items_id = db.Column(db.BigInteger, db.ForeignKey('ebay_items.id'), primary_key=True)
	measurement_value = db.Column(db.Integer)

	measurement_type = db.relationship('MeasurementType')

	def __repr__(self):
		return '<%r, %r>' % (self.measurement_type, self.measurement_value)


class MeasurementType(db.Model):
	__tablename__ = 'measurement_types'
	id = db.Column(db.Integer, primary_key=True)
	attribute = db.Column(db.Text())
	clothing_category = db.Column(db.Text())
	# There's also a combined UniqueConstraint set on attribute and clothing_combined.
	# I don't know how to represent that in the class.

	SUPPORTED_CATEGORIES_EBAY_VALUES = {3002: 'sportcoat'}

	def __repr__(self):
		return '<id: %r, clothing_category: %r, attribute: %r>' % (
			self.id, self.clothing_category, self.attribute)


class Item(db.Model):
	__tablename__ = 'ebay_items'
	id = db.Column(db.Integer, primary_key=True)
	ebay_item_id = db.Column(db.BigInteger, unique=False, nullable=False)  # explicitely False
	end_date = db.Column(db.DateTime, nullable=False)
	last_access_date = db.Column(db.DateTime, nullable=False)
	ebay_title = db.Column(db.Text(), nullable=False)
	ebay_primary_category = db.Column(db.Integer)
	current_price = db.Column(db.Integer)
	ebay_url = db.Column(db.Text())
	ebay_affiliate_url = db.Column(db.Text())

	internal_seller_id = db.Column(db.Integer, db.ForeignKey('ebay_sellers.id'), nullable=False)
	seller = db.relationship('EbaySeller', back_populates='items')

	measurements = db.relationship(
		'ItemMeasurementAssociation', cascade="all, delete-orphan")
	# sizes = None  # An association of all the sizes (and types) for this listing

	def __repr__(self):
		return '<ebay_item_id: %r, ebay_title: %r..., end_date: %r, last_access_date: %r>' % (
			self.ebay_item_id, self.ebay_title, str(self.end_date), str(self.last_access_date))


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
	size = db.Column(db.Text(), unique=True)

	def __repr__(self):
		return 'Casual shirt size "%r"' % (self.size)


# Size Key Table dict
model_directory_dict = {
	'shirt-sleeve': SizeKeyShirtDressSleeve,
	'shirt-neck': SizeKeyShirtDressNeck,
	'shirt-casual': SizeKeyShirtCasual
}



