#from wtforms import Form, StringField, PasswordField, validators
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf import FlaskForm

class RegistrationForm(FlaskForm):
	email = StringField('Email', validators=[
		Email(),
		Length(min=6, max=35),
		DataRequired()
	])
	password = PasswordField('New password', validators=[
		Length(min=6, max=35),
		EqualTo('confirm', message='Passwords must match'),
		DataRequired()
	])
	confirm = PasswordField('Repeat password')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[
		DataRequired(),
		Email()
	])
	password = PasswordField('Password', validators=[
		Length(min=6, max=35),
		DataRequired()
	])