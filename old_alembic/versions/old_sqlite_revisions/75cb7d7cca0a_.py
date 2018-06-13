"""Change the casual shirt table to have a uniform 'size' column like the other tables.

Revision ID: 75cb7d7cca0a
Revises: 0520ee6bf632
Create Date: 2018-05-16 16:39:43.857966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75cb7d7cca0a'
down_revision = '0520ee6bf632'
branch_labels = None
depends_on = None


def upgrade():
	op.rename_table('size_key_shirt_casual', 'old_casual')

	# Grab the old table
	old_table = sa.Table(
		'old_casual',
		sa.MetaData(),
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size_short', sa.Text(6)),
		sa.Column('size_long', sa.Text(20))
	)

	# Make a new table. Old size_short will be new 'size'.
	new_table = op.create_table(
		'size_key_shirt_casual',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Text(6)),
		sa.Column('size_long', sa.Text(20)),
		sa.UniqueConstraint('size', name='uq_size'),
		sa.UniqueConstraint('size_long', name='uq_size')
	)

	conn = op.get_bind()

	for row in conn.execute(old_table.select()):
		conn.execute(
			(
				new_table
				.insert()
				.values(id=row.id, size=row.size_short, size_long=row.size_long)
			)
		)

	op.drop_table('old_casual')


def downgrade():
	op.rename_table('size_key_shirt_casual', 'old_casual')

	# Grab the old table
	old_table = sa.Table(
		'old_casual',
		sa.MetaData(),
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Text(6)),
		sa.Column('size_long', sa.Text(20))
	)

	new_table = op.create_table(
		'size_key_shirt_casual',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size_short', sa.Text(6)),
		sa.Column('size_long', sa.Text(20)),
		sa.UniqueConstraint('size_short', name='uq_size'),
		sa.UniqueConstraint('size_long', name='uq_size')
	)

	conn = op.get_bind()

	for row in conn.execute(old_table.select()):
		conn.execute(
			(
				new_table
				.insert()
				.values(id=row.id, size_short=row.size, size_long=row.size_long)
			)
		)

	op.drop_table('old_casual')
