from flask import render_template, flash, redirect, session
from app import app, db
from .models import User

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')
