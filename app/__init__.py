from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery
from config import Config

from logging.handlers import RotatingFileHandler
import os
import sys
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
if not os.path.exists('logs'):
	os.mkdir('logs')

# The flask logger is called flask.app
# The top level that the rest of the code uses follows the directory naming and is 'app'
not_flask_logger = logging.getLogger('app')

# my strategy is to emit everything. pull everything out to a log file and siphon off
# useful stuff to console.
not_flask_logger.setLevel(logging.DEBUG)

long_log_format = logging.Formatter(
	'%(asctime)s [%(levelname)s] %(name)s: %(message)s [in %(pathname)s:%(lineno)d]')
short_log_format = logging.Formatter(
	'[%(levelname)s] %(name)s --- %(message)s')

file_handler = RotatingFileHandler('logs/ltf.log', maxBytes=5*1024*1024, backupCount=10)
file_handler.setFormatter(long_log_format)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(short_log_format)
console_handler.setLevel(logging.INFO)

not_flask_logger.addHandler(file_handler)
not_flask_logger.addHandler(console_handler)

app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)

if app.debug:
	app.logger.setLevel(logging.DEBUG)
	console_handler.set_level(logging.DEBUG)

app.logger.info('LTF startup')
