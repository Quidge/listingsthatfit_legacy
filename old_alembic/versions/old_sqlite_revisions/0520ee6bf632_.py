"""Adding unique composite constraints to columns in association tables. It should
not be possible to have a user associated with a size twice.

Revision ID: 0520ee6bf632
Revises: c7ae1554d68a
Create Date: 2018-05-12 12:59:37.882382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0520ee6bf632'
down_revision = 'c7ae1554d68a'
branch_labels = None
depends_on = None


def upgrade():

	#####
	# SHIRT NECK ASSOCIATION TABLE
	#####

	# Rename old link table
	op.rename_table('link_user_size_shirt_dress_neck', 'old_link1')

	# Grab old link table
	old_link1 = sa.Table(
		'old_link1',
		sa.MetaData(),
		sa.Column('size_id'),
		sa.Column('user_id')
	)

	# Create new table
	new_link1 = op.create_table(
		'link_user_size_shirt_dress_neck',
		sa.Column(
			'size_id',
			sa.Integer,
			sa.ForeignKey('size_key_shirt_dress_neck.id'),
			nullable=False,
			primary_key=True,
		),
		sa.Column(
			'user_id',
			sa.Integer,
			sa.ForeignKey('user.id'),
			nullable=False,
			primary_key=True
		),
		sa.UniqueConstraint('size_id', 'user_id', name='uq_association')
	)

	# Open connection
	conn = op.get_bind()

	# Fill columns in new table with for loop because I'm scared of using op.bulk_insert
	for row in conn.execute(old_link1.select()):
		conn.execute(new_link1.insert().values(size_id=row.size_id, user_id=row.user_id))

	# Drop the old table
	op.drop_table('old_link1')

	####
	# SHIRT CASUAL ASSOCIATION TABLE
	####

	# Rename old link table
	op.rename_table('link_user_size_shirt_casual', 'old_link2')

	# Grab old link table
	old_link2 = sa.Table(
		'old_link2',
		sa.MetaData(),
		sa.Column('size_id'),
		sa.Column('user_id')
	)

	# Create new table
	new_link1 = op.create_table(
		'link_user_size_shirt_casual',
		sa.Column(
			'size_id',
			sa.Integer,
			sa.ForeignKey('size_key_shirt_casual.id'),
			nullable=False,
			primary_key=True,
		),
		sa.Column(
			'user_id',
			sa.Integer,
			sa.ForeignKey('user.id'),
			nullable=False,
			primary_key=True
		),
		sa.UniqueConstraint('size_id', 'user_id', name='uq_association')
	)

	# Open connection
	conn = op.get_bind()

	# Fill columns in new table with for loop because I'm scared of using op.bulk_insert
	for row in conn.execute(old_link2.select()):
		conn.execute(new_link1.insert().values(size_id=row.size_id, user_id=row.user_id))

	# Drop the old table
	op.drop_table('old_link2')

def downgrade():
	"""
	Same as before, but in this case the new link table doesn't have a unique
	constraint applied.
	"""

	# Rename old link table
	op.rename_table('link_user_size_shirt_dress_neck', 'old_link1')

	# Grab old link table
	old_link1 = sa.Table(
		'old_link1',
		sa.MetaData(),
		sa.Column('size_id'),
		sa.Column('user_id')
	)

	# Create new table
	new_link1 = op.create_table(
		'link_user_size_shirt_dress_neck',
		sa.Column(
			'size_id',
			sa.Integer,
			sa.ForeignKey('size_key_shirt_dress_neck.id'),
			nullable=False,
			primary_key=True,
		),
		sa.Column(
			'user_id',
			sa.Integer,
			sa.ForeignKey('user.id'),
			nullable=False,
			primary_key=True
		)
	)

	# Open connection
	conn = op.get_bind()

	# Fill columns in new table with for loop because I'm scared of using op.bulk_insert
	for row in conn.execute(old_link1.select()):
		conn.execute(new_link1.insert().values(size_id=row.size_id, user_id=row.user_id))

	# Drop the old table
	op.drop_table('old_link1')

	####
	# SHIRT CASUAL ASSOCIATION TABLE
	####

	# Rename old link table
	op.rename_table('link_user_size_shirt_casual', 'old_link2')

	# Grab old link table
	old_link2 = sa.Table(
		'old_link2',
		sa.MetaData(),
		sa.Column('size_id'),
		sa.Column('user_id')
	)

	# Create new table
	new_link1 = op.create_table(
		'link_user_size_shirt_casual',
		sa.Column(
			'size_id',
			sa.Integer,
			sa.ForeignKey('size_key_shirt_casual.id'),
			nullable=False,
			primary_key=True,
		),
		sa.Column(
			'user_id',
			sa.Integer,
			sa.ForeignKey('user.id'),
			nullable=False,
			primary_key=True
		)
	)

	# Open connection
	conn = op.get_bind()

	# Fill columns in new table with for loop because I'm scared of using op.bulk_insert
	for row in conn.execute(old_link2.select()):
		conn.execute(new_link1.insert().values(size_id=row.size_id, user_id=row.user_id))

	# Drop the old table
	op.drop_table('old_link2')







