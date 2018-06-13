"""change shirt size key table's size fields from decimal to integer

Revision ID: 5591a1224fed
Revises: 
Create Date: 2018-04-16 12:01:09.868529

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5591a1224fed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

	conn = op.get_bind()

	# define helper table
	dec_to_int_helper_table = sa.Table(
		'size_key_shirt_dress_sleeve',
		sa.MetaData(),
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Numeric(4, 2)),
		sa.Column('sizeasint', sa.Integer),
	)

	# add new integer conversion column to old_table
	op.add_column(
		'size_key_shirt_dress_sleeve',
		sa.Column('sizeasint', sa.Integer)
	)

	# populate new column by converting values from old column
	for row in conn.execute(dec_to_int_helper_table.select()):
		dec_val = row.size
		int_val = int(dec_val * 100)
		conn.execute(
			(
				dec_to_int_helper_table
				.update()
				.where(dec_to_int_helper_table.c.id == row.id)
				.values(sizeasint=int_val)
			)
		)

	# create a holding table and store it for use later
	temp_table = op.create_table(
		'temp_sleeve_backup',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('sizeasint', sa.Integer)
	)

	# copy over values from old_table to temp table
	for row in conn.execute(dec_to_int_helper_table.select()):
		conn.execute(temp_table.insert().values(id=row.id, sizeasint=row.sizeasint))

	# drop the old_table
	op.drop_table('size_key_shirt_dress_sleeve')

	# create a new table with the same name, but this one has only the columns we want
	new_table = op.create_table(
		'size_key_shirt_dress_sleeve',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer)
	)

	# copy values from temp table into new table
	for row in conn.execute(temp_table.select()):
		conn.execute(new_table.insert().values(id=row.id, size=row.sizeasint))

	# drop temp table
	op.drop_table('temp_sleeve_backup')


# this will do the above but in reverse. same process.
def downgrade():
	from decimal import Decimal

	conn = op.get_bind()

	# define helper table
	int_to_dec_helper_table = sa.Table(
		'size_key_shirt_dress_sleeve',
		sa.MetaData(),
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer),
		sa.Column('sizeasdec', sa.Numeric(4, 2)),
	)

	# add new column to prep for decimal values
	op.add_column(
		'size_key_shirt_dress_sleeve',
		sa.Column('sizeasdec', sa.Numeric(4, 2))
	)

	# now all columns exist in DB as defined in helper table, so select() will run
	# without whining that it can't find a column

	# convert extant integer values to decimal representations.
	# with these new values, populate the new column
	for row in conn.execute(int_to_dec_helper_table.select()):
		int_val = row.size
		dec_val = Decimal(int_val) / 100
		conn.execute(
			(
				int_to_dec_helper_table
				.update()
				.where(int_to_dec_helper_table.c.id == row.id)
				.values(sizeasdec=dec_val)
			)
		)

	# create a holding table and store it for use later
	temp_table = op.create_table(
		'temp_sleeve_to_dec',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('sizeasdec', sa.Numeric(4, 2))
	)

	# copy over values from old_table to temp table
	for row in conn.execute(int_to_dec_helper_table.select()):
		conn.execute(temp_table.insert().values(id=row.id, sizeasdec=row.sizeasdec))

	# drop the old table
	op.drop_table('size_key_shirt_dress_sleeve')

	# create a new table with the same name, but this one only has the columns we want
	new_table = op.create_table(
		'size_key_shirt_dress_sleeve',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Numeric(4, 2))
	)

	for row in conn.execute(temp_table.select()):
		conn.execute(new_table.insert().values(id=row.id, size=row.sizeasdec))

	# drop temp table
	op.drop_table('temp_sleeve_to_dec')


















