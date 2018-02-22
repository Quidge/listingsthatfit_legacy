from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(32), unique=False)

	def __repr__(self):
		return '<User id: %r, email: %r, password: %r>' % (self.id, self.email, self.password)

