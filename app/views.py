from flask import render_template, flash, redirect, session, request
from flask_login import login_user, logout_user, login_required
from app import app, db, lm
from app.models import User
from app.forms import RegistrationForm, LoginForm
from wtforms.validators import ValidationError

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

@lm.user_loader
def user_loader(user_id):
	"""Given *user_id*, return the associated User object."""
	return User.query.get(user_id)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/preferences')
@login_required
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

	if request.method == "POST":
		if not form.validate():
			flash_errors(form)
			return render_template('login.html', form=form)

		user = User.query.filter_by(email=form.email.data).first()

		if not user:
			flash("Cannot find an account under %s" % form.email.data)
			return render_template('login.html', form=form)
		elif not user.verify_password(form.password.data):
			flash("Incorrect password")
			return render_template('login.html', form=form)
		else:
			login_user(user)
			return redirect('/index')

	else:
		return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Register a new user account."""

	form = RegistrationForm(request.form)

	if request.method == "POST":
		if not form.validate():
			flash_errors(form)
			return render_template('register.html', form=form)

		user = User(email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)

		flash("Account created successfully!")

		return render_template('index.html')

	else:
		return render_template('register.html', form=form)

