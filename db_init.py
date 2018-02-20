from flask_sqlalchemy import SQLAlchemy
from helpers import get_env_variable
from flask import Flask

app = Flask(__name__)

PG_URL = get_env_variable('PGDATA')
PG_USER = get_env_variable('POSTGRES_USER')
PG_PASSWORD = get_env_variable('POSTGRES_PW')
PG_DB = get_env_variable('POSTGRES_DB')


DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
	user=PG_USER, pw=PG_PASSWORD, url=PG_URL, db=PG_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)