from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
link_user_size_shirt_dress_sleeve = Table('link_user_size_shirt_dress_sleeve', post_meta,
    Column('size_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, primary_key=True, nullable=False),
)

size_key_shirt_sleeve = Table('size_key_shirt_sleeve', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('size', Numeric(precision=4, scale=2)),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('email', VARCHAR(length=120)),
    Column('password_hash', VARCHAR(length=32)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=120)),
    Column('password', String(length=32)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['link_user_size_shirt_dress_sleeve'].create()
    post_meta.tables['size_key_shirt_sleeve'].create()
    pre_meta.tables['user'].columns['password_hash'].drop()
    post_meta.tables['user'].columns['password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['link_user_size_shirt_dress_sleeve'].drop()
    post_meta.tables['size_key_shirt_sleeve'].drop()
    pre_meta.tables['user'].columns['password_hash'].create()
    post_meta.tables['user'].columns['password'].drop()
