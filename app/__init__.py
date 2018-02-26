from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_envvar('DEV_CONFIG_SETTINGS')

lm = LoginManager()
lm.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, views