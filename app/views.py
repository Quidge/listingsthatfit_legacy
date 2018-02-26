from flask import render_template, flash, redirect, session, request
from flask_login import login_user
from app import app, db, lm
from app.models import User
from app.forms import RegistrationForm

@lm.user_loader
def user_loader(user_id):
	"""Given *user_id*, return the associated User object."""
	return User.query.get(id)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Log user in"""

	'''form = RegistrationForm(request.form)

	if request.method == "POST" and form.validate():
		user = User(email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)

		flash("Account created successfully!")

		return render_template('index.html')

		# Form validating (replace with WTF form login template soon)
		if not request.form.get("email"):
			flash('Missing email')
			return render_template("login.html")
		elif not request.form.get("password"):
			flash('Missing password')
			return render_template("login.html")
	else:
		return render_template('login.html')

	email = request.form.get("email")'''

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Register a new user account."""

	form = RegistrationForm(request.form)

	if request.method == "POST" and form.validate():
		user = User(email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)

		flash("Account created successfully!")

		return render_template('index.html')
	
	elif not form.validate():
		flash("Form failed")

	return render_template('register.html', form=form)



