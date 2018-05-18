from flask import render_template, flash, redirect, session, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select

from app import app, db, lm
from app.models import User, SizeKeyShirtDressSleeve, LinkUserSizeShirtDressSleeve
from app.forms import RegistrationForm, LoginForm
from app.utils import SUPPORTED_CLOTHING, cat_size_prefs
from app.utils import diff_preference_changes, get_user_sizes_subscribed
from app.dbtouch import get_user_sizes_join_with_all_possible, update_user_sizes

from app.utils import int_to_decimal

# Custom filter
app.jinja_env.filters["int_to_decimal"] = int_to_decimal


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


@app.route('/preferences/')
@login_required
def preferences():
	return redirect('/preferences/sizes')

'''@app.route('/preferences/clothing/<category>')
@login_required
def preferences_clothing(category):
	category = str.lower(category)

	user_sizes = {}

	if category == 'shirts':
		user_sizes = {
			"sleeves": current_user.sz_shirt_dress_sleeve,
			"necks": current_user.sz_shirt_dress_neck,
			"casuals": current_user.sz_shirt_casual
		}
		#user_sizes.sleeves = current_user.sz_shirt_dress_sleeve
		#user_sizes.neck = current_user.sz_shirt_dress_neck
		#user_sizes.casual = current_user.sz_shirt_casual

	if category in SUPPORTED_CLOTHING:
		return render_template('/preferences/clothing/{}.html'.format(category),
			user_sizes=user_sizes)
	else:
		return redirect(404)'''


@app.route('/preferences/sizes', methods=["GET", "POST"])
@login_required
def clothing_preferences_settings():

	user_sizes = get_user_sizes_join_with_all_possible(current_user)
	user_subscribed_sizes = get_user_sizes_subscribed(current_user)

	if request.method == "POST":
		''' The situation if POSTed should be a user attempted to update size preferences.
		So, request should hold some object that contains the new additions(?) and update
		the DB. After DB is updated, re-serve the page with updated user preferences.
		'''

		''' Update process:
			- Compose presence/lack of input values from form AND user_sizes to build a dict with the NEW updated values.
				- update dict format is:
					{size_specific: [list of values],
					...,
					next_size_specific: [list of values]}
			--		
			IF differences detected between user_sizes and new sizes, then proceed
			--
			- Pass this new 'update values' dict to a function that:
				- Parses the dict
				- Determines which tables to update
				- Updates table
				- Commits session
			- Re-query for sizes
			- Re-serve page
		'''

		f = request.form
		ready_for_diffing = {}

		for key in f.keys():
			ready_for_diffing[key] = [int(val) if val.isdigit() else val for val in f.getlist(key)]

		diffs_from_db = diff_preference_changes(user_subscribed_sizes, ready_for_diffing)
		update_user_sizes(diffs_from_db, current_user)
		db.session.commit()

		user_sizes = get_user_sizes_join_with_all_possible(current_user)

	return render_template('/preferences/user_sizes_settings.html', user_sizes=user_sizes)


@app.route('/preferences/seller_subscriptions', methods=["GET"])
@login_required
def seller_subscription_settings():
	user_subbed = [seller for seller in current_user.user_subbed]

	return render_template('/preferences/seller_subscription_settings.html', user_subbed=user_subbed)


@app.route('/preferences/notifications', methods=["GET"])
@login_required
def notification_settings():
	return render_template('/preferences/notification_settings.html')


@app.route('/preferences/account', methods=["GET"])
@login_required
def account_settings():
	return render_template('/preferences/account_settings.html')


@app.route('/preferences/password', methods=["GET"])
@login_required
def password_settings():
	return render_template('/preferences/password_settings.html')


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

