from flask import render_template, flash, redirect, session, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select

from app import app, db, lm
from app.models import User, SizeKeyShirtDressSleeve, LinkUserSizeShirtDressSleeve
from app.forms import RegistrationForm, LoginForm
from app.utils import SUPPORTED_CLOTHING, cat_size_prefs
from app.utils import diff_preference_changes, get_user_sizes_subscribed
from app.dbtouch import update_user_sizes, get_user_sizes_join_with_all_possible

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

@app.route('/preferences')
@login_required
def preferences():
	#return redirect('/preferences/clothing/suits')
	return redirect('/preferences/clothing')

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

@app.route('/preferences/clothing', methods=["GET", "POST"])
@login_required
def preferences_clothing():

	'''
	I have to figure out how to recreate this query with SQLAlchemy:

	select 	
		size, 
   		case 	when link_user_size_shirt_dress_sleeve.size_id is not null 
   				then 'true' else 'false' end as present
		from size_key_shirt_dress_sleeve 
		left join link_user_size_shirt_dress_sleeve
		on size_key_shirt_dress_sleeve.id = link_user_size_shirt_dress_sleeve.size_id
	;
	'''
	'''
	user_link_table = (select([LinkUserSizeShirtDressSleeve])
		.where(LinkUserSizeShirtDressSleeve.c.user_id==current_user.id)
		.alias())

	shirt_sleeve_sizes = (db.session
		.query(SizeKeyShirtDressSleeve.size, user_link_table.c.size_id != None)
		.outerjoin(user_link_table, user_link_table.c.size_id == SizeKeyShirtDressSleeve.id)
		.all())

	user_sizes = {
		"Shirting": {
			"Sleeve": {"values": dict(shirt_sleeve_sizes), "cat_key": "shirt-dress-sleeve"}
			#"necks": current_user.sz_shirt_dress_neck,
			#"casuals": current_user.sz_shirt_casual
		}
	}
	'''
	user_sizes = get_user_sizes_join_with_all_possible(current_user)
	stuff = get_user_sizes_subscribed(current_user)

	print(user_sizes)
	print('---')
	print(stuff)
	#print(stuff)

	#for key, values in stuff.items():
	#	val_list = [val.size for val in values]
	#	print(key, ": ", val_list)

	# print(dict(shirt_sleeve_sizes))
	# for key, value in dict(shirt_sleeve_sizes).items():
	#	print(key,":",value)

	if request.method == "POST":
		''' The situation if POSTed should be a user attempted to update size preferences.
		So, request should hold some object that contains the new additions(?) and update
		the DB. After DB is updated, re-serve the page with updated user preferences.
		'''

		''' Update process:
			- Compose presence/lack of input values from form AND user_sizes to build a dict with the NEW updated values.
				- update dict format is {size_cat: {size_specific: [list of values]}} 	
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
		# Composes dict of updates.
		# updates_dict is to have the form: {size_cat: {size_specific: [list of tuples in format (size_val, true/false for added/removed)]}}
		# get_pref_updates must be passed user_sizes, because request.form WILL NOT return checkboxes that have been UNCHECKED. the absence of a value when present in user_sizes indicates that the user wishes to REMOVE the size from their preferences
		# updates_dict = diff_preference_changes(user_sizes, request.form)

		# touches the database
		# update_user_sizes(updates_dict, current_user)

		# this will be new user sizes (also touches the database)
		# user_sizes = get_user_sizes(current_user)
		# print(user_sizes["Shirting"]["Sleeve"]["values"])

		#for key, val_list in stuff.items():
		#	print(key, ": ", val_list)

		updated_prefs = {}
		f = request.form

		for key in f.keys():
			updated_prefs[key] = [int(val) if val.isdigit() else val for val in f.getlist(key)]

		print('updated: ', updated_prefs)
		#print(diff_preference_changes(stuff, updated_prefs))
		print(diff_preference_changes(stuff, updated_prefs))

		#f = request.form
		#for key in f.keys():
		#	# for value in f.getlist(key):
		#	#	print(key, ":", value)
		#	print(key, ":", f.getlist(key))

	return render_template('/preferences/user_sizes.html', user_sizes=user_sizes)


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

