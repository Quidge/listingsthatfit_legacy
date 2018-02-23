from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(32), unique=False)

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

