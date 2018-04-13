from flask import render_template, flash, redirect, session, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, lm
from app.models import User, SizeKeyShirtDressSleeve, LinkUserSizeShirtDressSleeve
from app.forms import RegistrationForm, LoginForm
from app.utils import SUPPORTED_CLOTHING, cat_size_prefs
from sqlalchemy import select

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

	user_link_table = (select([LinkUserSizeShirtDressSleeve])
		.where(LinkUserSizeShirtDressSleeve.c.user_id==current_user.id)
		.alias())

	shirt_sleeve_sizes = (db.session
		.query(SizeKeyShirtDressSleeve.size, user_link_table.c.size_id != None)
		.outerjoin(user_link_table, user_link_table.c.size_id == SizeKeyShirtDressSleeve.id)
		.all())

	user_sizes = {
		"Shirting": {
			"Sleeve": {"sizes": dict(shirt_sleeve_sizes), "cat": "shirt-dress-sleeve"}
			#"necks": current_user.sz_shirt_dress_neck,
			#"casuals": current_user.sz_shirt_casual
		}
	}

	#print(dict(shirt_sleeve_sizes))
	#for key, value in dict(shirt_sleeve_sizes).items():
	#	print(key,":",value)

	if request.method == "POST":
		''' The situation if POSTed should be a user attempted to update size preferences.
		So, request should hold some object that contains the new additions(?) and update the DB.
		After DB is updated, re-serve the page with updated user preferences.
		'''

		''' Update process:
			- Compose presence/lack of input values from form AND user_sizes to build a dict with the NEW updated values.
				- update dict format is {size_cat: {size_specific: [list of values]}} 
			- Pass this new 'update values' dict to a function that:
				- Parses the dict
				- Determines which tables to update
				- Updates table
				- Commits session
			- Re-query for sizes
			- Re-serve page
		'''


		f = request.form
		for key in f.keys():
			for value in f.getlist(key):
				print(key,":",value)

		

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

