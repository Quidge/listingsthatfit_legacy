from wtforms import Form, StringField, PasswordField, validators

class RegistrationForm(Form):
	email = StringField('Email address', [
		validators.Length(min=6, max=35),
		validators.DataRequired()
	])
	password = PasswordField('New password', [
		validators.Length(min=6, max=35),
		validators.EqualTo('confirm', message='Passwords must match'),
		validators.DataRequired()
	])
	confirm = PasswordField('Repeat password')

class LoginForm(Form):
	email = StringField('Email address', [validators.DataRequired()])
	password = PasswordField('Password', [
		validators.Length(min=6, max=35),
		validators.DataRequired()
	])