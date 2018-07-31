import os

#basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('..', 'app.db')
# SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/ltf_db'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SECRET_KEY = 'this one' # change to hash at some point

class Config(object):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/ltf_db'
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'this one'
	SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/ltf_db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

