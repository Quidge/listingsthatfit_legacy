"""Add unique constraints to size key tables. (>1 entry for the numerical size shouldn't be possible

Revision ID: cb27d05c41b8
Revises: 929822e572b8
Create Date: 2018-04-29 14:00:17.072224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb27d05c41b8'
down_revision = '929822e572b8'
branch_labels = None
depends_on = None


def upgrade():
	# Rename table to allow creation of new table with constraint
	op.rename_table('size_key_shirt_dress_neck', 'old_neck')

	# Grab this old table
	old_table = sa.Table(
		'old_neck',
		sa.MetaData(),
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer)
	)

	# Create new table with constraint
	new_table = op.create_table(
		'size_key_shirt_dress_neck',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer),
		sa.UniqueConstraint('size', name='uq_size')
	)

	# Open connection
	conn = op.get_bind()

	# Fill columns in new table with for loop because I'm scared of using op.bulk_insert
	for row in conn.execute(old_table.select()):
		conn.execute(new_table.insert().values(id=row.id, size=row.size))

	# Drop the old table
	op.drop_table('old_neck')


def downgrade():
	op.rename_table('size_key_shirt_dress_neck', 'old_neck')

	old_table = sa.Table(
		'old_neck',
		sa.MetaData(),
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer)
	)

	new_table = op.create_table(
		'size_key_shirt_dress_neck',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer)
	)

	conn = op.get_bind()

	for row in conn.execute(old_table.select()):
		conn.execute(new_table.insert().values(id=row.id, size=row.size))

	op.drop_table('old_neck')
