"""change shirt size key table's size fields from decimal to integer

Revision ID: 5591a1224fed
Revises: 
Create Date: 2018-04-16 12:01:09.868529

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import INTEGER, Column
from decimal import Decimal


# revision identifiers, used by Alembic.
revision = '5591a1224fed'
down_revision = None
branch_labels = None
depends_on = None


decimal_to_int_helper_shirt_sleeve = sa.Table(
	'size_key_shirt_dress_sleeve',
	sa.MetaData(),
	sa.Column('id', sa.Integer, primary_key=True),
	sa.Column('size', sa.Numeric(4, 2)),
	sa.Column('sizeasint', sa.Integer)
)


def upgrade():
	conn = op.get_bind()

	op.add_column(
		'size_key_shirt_dress_sleeve',
		sa.Column('sizeasint', sa.Integer)
	)

	for row in conn.execute(decimal_to_int_helper_shirt_sleeve.select()):
		dec_val = row.size
		int_val = int(dec_val * 100)
		conn.execute(decimal_to_int_helper_shirt_sleeve.update().where(decimal_to_int_helper_shirt_sleeve.c.id == row.id).values(sizeasint=int_val))

	# create temp table

	op.create_table(
		'temp_sleeve_backup',
		Column('id', INTEGER, primary_key=True),
		Column('size', INTEGER)
	)

	temp_table = sa.Table(
		'temp_sleeve_backup',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer)
	)

	# copy id, sizeasint from decimal_to_in_helper_shirt_sleeve to temp table

	for row in conn.execute(decimal_to_int_helper_shirt_sleeve.select()):
		conn.execute(temp_table.insert().values(id=temp_table.id, size=temp_table.size))

	# drop size_key_shirt_dress_sleeve

	# create another size_key_shirt_dress_sleeve table with only id, size rows

	# populate new size_key_shirt_dress_sleeve with values from temp_table

	# drop temp table

	op.drop_column('size_key_shirt_dress_sleeve', 'size')

	op.alter_column(
		'size_key_shirt_dress_sleeve',
		'sizeasint',
		new_column_name='size'
	)

	# create new column ('tempname') that is old_col*100
	# drop 'size'
	# rename 'tempname' to 'size'


def downgrade():
	'''conn = op.get_bind()

	op.add_column(
		'size_key_shirt_dress_sleeve',
		sa.Column('sizeasdec', sa.Numeric(4, 2))
	)

	for row in conn.execute(decimal_to_int_helper_shirt_sleeve.select()):
		int_val = row.size
		dec_val = Decimal(int_val) / Decimal(100)
		conn.execute(decimal_to_int_helper_shirt_sleeve.update().where(decimal_to_int_helper_shirt_sleeve.c.id == row.id).values(sizeasdec=dec_val))

	op.drop_column('size_key_shirt_dress_sleeve', 'size')

	op.alter_column(
		'size_key_shirt_dress_sleeve',
		'sizeasdec',
		new_column_name='size')'''
	pass

