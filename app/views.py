from flask import render_template, flash, redirect, session, request
from flask_login import login_user, logout_user, login_required
from app import app, db, lm
from app.models import User
from app.forms import RegistrationForm, LoginForm

@lm.user_loader
def user_loader(user_id):
	"""Given *user_id*, return the associated User object."""
	return User.query.get(id)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

'''@app.route('/preferences')
@lm.login_required
def preferences():'''

@app.route('/preferences')
@lm.login_required
def preferences():
	return redirect('/preferences/clothing/suits')

@app.route('/preferences/clothing/<category>')
def preferences_clothing(category):
	category = tolower(category)

	if category in ['suits', 'sportcoats', 'shirts', 'shoes', 'outerwear', 'pants']:
		return render_template('/preferences/clothing/%s.html' % category,
			sizes=user_sizes, brands=user_brands)
	else:
		return abort(404)



@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Log user in"""

	form = LoginForm(request.form)

	if request.method == "POST" and form.validate():
		user = User.query.filter_by(email=form.email.data).first_or_404()
		if user.verify_password(form.password.data):
			login_user(user)
			return redirect('index.html')
		else:
			flash('Incorrect email or password.')
			return redirect('login.html')
	else:
		return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('login.html')


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

