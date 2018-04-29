"""Change shirt neck size key table from decimal sizes to integer

Revision ID: 929822e572b8
Revises: 5591a1224fed
Create Date: 2018-04-29 13:06:27.145096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '929822e572b8'
down_revision = '5591a1224fed'
branch_labels = None
depends_on = None


def upgrade():

	conn = op.get_bind()

	# Define this table so it can hold both decimal and integer sizes.
	# However, until we create it below, the sizeasint column does not currently
	# exist in the DB. It is only part of our abstraction.
	dec_to_int_helper = sa.Table(
		'size_key_shirt_dress_neck',
		sa.MetaData(),
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Numeric(4, 2)),
		sa.Column('sizeasint', sa.Integer)
	)

	# Make that abstraction real and add a real column to the table in DB.
	op.add_column(
		'size_key_shirt_dress_neck',
		sa.Column('sizeasint', sa.Integer)
	)

	# Now let's populate the column we just created with integer representations of
	# the sizes (which are now currently only in decimal).

	# Quick note, if we hadn't paired up the helper table pseudo column 'sizeasint'
	# with a real column, select() would fail here.
	for row in conn.execute(dec_to_int_helper.select()):
		dec_val = row.size
		int_val = int(dec_val * 100)
		conn.execute(
			(
				dec_to_int_helper
				.update()
				.where(dec_to_int_helper.c.id == row.id)
				.values(sizeasint=int_val)
			)
		)

	# SQLite does not support 'DROP TABLE' SQL commands. The old decimal sizes column
	# needs to go. To get it gone, we're going to:
	# 1) create a temp table with
	# 2) copy only the columns we want to keep (id, sizeasint) into the temp table
	# 3) drop the original table (can't have two tables with the same name)
	# 4) recreate the original table with ONLY the columns we want: (id, sizeasint)
	# 5) copy temp table values into new size_key_shirt_dress_neck
	# 6) drop temp teable

	# Create a temp table
	temp_table = op.create_table(
		'temp_neck_to_int',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('sizeasint', sa.Integer)
	)

	# Copy over columns from old size_neck table into temp table
	for row in conn.execute(dec_to_int_helper.select()):
		conn.execute(temp_table.insert().values(id=row.id, sizeasint=row.sizeasint))

	# Drop the old table
	op.drop_table('size_key_shirt_dress_neck')

	# Creatre a new table with the same name, but that only has the columns we want
	new_table = op.create_table(
		'size_key_shirt_dress_neck',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer)
	)

	# Copy values from temp table into the new table
	for row in conn.execute(temp_table.select()):
		conn.execute(new_table.insert().values(id=row.id, size=row.sizeasint))

	# Drop the temp table
	op.drop_table('temp_neck_to_int')


def downgrade():

	# This is simply the reverse of the above. Everything is the same except that we
	# must import Decimal.

	from decimal import Decimal

	conn = op.get_bind()

	# Define the helper table
	int_to_dec_helper = sa.Table(
		'size_key_shirt_dress_neck',
		sa.MetaData(),
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer),
		sa.Column('sizeasdec', sa.Numeric(4, 2))
	)

	# Add new column the the actual, in DB, table
	op.add_column(
		'size_key_shirt_dress_neck',
		sa.Column('sizeasdec', sa.Numeric(4, 2))
	)

	# Convert extant integer values into decimal representations.
	# With these new values, populate the new decimal size column.

	for row in conn.execute(int_to_dec_helper.select()):
		int_val = row.size
		dec_val = Decimal(int_val) / 100
		conn.execute(
			(
				int_to_dec_helper
				.update()
				.where(int_to_dec_helper.c.id == row.id)
				.values(sizeasdec=dec_val)
			)
		)

	# Create a temporary table
	temp_table = op.create_table(
		'temp_neck_to_dec',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('sizeasdec', sa.Numeric(4, 2))
	)

	# Copy over values from the old table into the temp table
	for row in conn.execute(int_to_dec_helper.select()):
		conn.execute(temp_table.insert().values(id=row.id, sizeasdec=row.sizeasdec))

	# Drop the old table
	op.drop_table('size_key_shirt_dress_neck')

	# Create a new table with the same name, but this one only has the columns we want.
	new_table = op.create_table(
		'size_key_shirt_dress_neck',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Numeric(4, 2))
	)

	# This is susceptible to weird ordering. If at some point in the future the values
	# for temp_table.select() arent in mixed order, they won't map correctly in this
	# step. Dangerous.
	for row in conn.execute(temp_table.select()):
		conn.execute(new_table.insert().values(id=row.id, size=row.sizeasdec))

	# Drop temp table
	op.drop_table('temp_neck_to_dec')












