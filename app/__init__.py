from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_envvar('DEV_CONFIG_SETTINGS')
db = SQLAlchemy(app)

from app import models, views