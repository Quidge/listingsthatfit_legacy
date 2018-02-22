#from migrate.versioning import api

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

print(db)

db.create_all()
print('executed fine')