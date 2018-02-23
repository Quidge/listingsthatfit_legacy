from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
size_key_shirt_sleeve = Table('size_key_shirt_sleeve', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('size', NUMERIC(precision=4, scale=2)),
)

link_user_size_shirt_casual = Table('link_user_size_shirt_casual', post_meta,
    Column('size_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, primary_key=True, nullable=False),
)

link_user_size_shirt_dress_neck = Table('link_user_size_shirt_dress_neck', post_meta,
    Column('size_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, primary_key=True, nullable=False),
)

size_key_shirt_casual = Table('size_key_shirt_casual', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('size_short', Text(length=6)),
    Column('size_long', Text(length=20)),
)

size_key_shirt_dress_neck = Table('size_key_shirt_dress_neck', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('size', Numeric(precision=4, scale=2)),
)

size_key_shirt_dress_sleeve = Table('size_key_shirt_dress_sleeve', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('size', Numeric(precision=4, scale=2)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['size_key_shirt_sleeve'].drop()
    post_meta.tables['link_user_size_shirt_casual'].create()
    post_meta.tables['link_user_size_shirt_dress_neck'].create()
    post_meta.tables['size_key_shirt_casual'].create()
    post_meta.tables['size_key_shirt_dress_neck'].create()
    post_meta.tables['size_key_shirt_dress_sleeve'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['size_key_shirt_sleeve'].create()
    post_meta.tables['link_user_size_shirt_casual'].drop()
    post_meta.tables['link_user_size_shirt_dress_neck'].drop()
    post_meta.tables['size_key_shirt_casual'].drop()
    post_meta.tables['size_key_shirt_dress_neck'].drop()
    post_meta.tables['size_key_shirt_dress_sleeve'].drop()
