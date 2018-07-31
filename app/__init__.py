from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery
from config import Config

from logging.handlers import RotatingFileHandler
import os
import logging

app = Flask(__name__)
# app.config.from_envvar('DEV_CONFIG_SETTINGS')
app.config.from_object(Config)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

db = SQLAlchemy(app)

from app import models, views

'''celery = Celery(
	app.name,
	broker='ampq://localhost',
	backend='ampq://',
	include=['app.celery_tasks']
)'''

# logging
if not app.debug:
	if not os.path.exists('logs'):
		os.mkdir('logs')
	fh = RotatingFileHandler('logs/ltf.log', maxBytes=10240, backupCount=10)
	fh.setFormatter(
		logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	fh.setLevel(logging.INFO)
	app.logger.addHandler(fh)

	app.logger.setLevel(logging.INFO)
	app.logger.info('LTF startup')
