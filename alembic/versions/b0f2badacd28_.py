"""Added store_url and items_url to EbaySellers model

Revision ID: b0f2badacd28
Revises: dd77025f2d77
Create Date: 2018-05-18 09:58:15.060917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0f2badacd28'
down_revision = 'dd77025f2d77'
branch_labels = None
depends_on = None


def upgrade():
	all_items = sa.Column('all_items_url', sa.Text(255), unique=False, nullable=True)

	# I have an itching feeling that maybe an actual person would have two seller accounts,
	# but only run a store on one of those accounts.
	# Also, not all sellers will have stores.

	# On second thought, it seems wise to always allow URLs to be nullable and non-unique.
	# I can't control the end output of a URL.
	store_url = sa.Column('store_url', sa.Text(255), unique=False, nullable=True)

	#op.add_column('ebay_sellers', all_items)
	#op.add_column('ebay_sellers', store_url)

	# SQLite really beginning to get on my nerves. It isn't possible to add a NOT NULL column
	# onto a table EVEN WHEN the table is empty.
	# https://stackoverflow.com/questions/3170634/how-to-solve-cannot-add-a-not-null-column-with-default-value-null-in-sqlite3

	op.rename_table('ebay_sellers', 'old_table')

	op.create_table(
		'ebay_sellers',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('seller_id', sa.Text(255), nullable=False, unique=True),
		all_items,
		store_url,
	)

	op.drop_table('old_table')


def downgrade():
	# SQLite does not support DROP COLUMN. This dance is necessary because of that.
	op.rename_table('ebay_sellers', 'old_table')

	old_table = sa.Table(
		'old_table',
		sa.MetaData(),
		sa.Column('id'),
		sa.Column('seller_id')
	)

	new_table = op.create_table(
		'ebay_sellers',
		sa.Column('id', sa.Integer),
		sa.Column('seller_id', sa.Text(255), unique=True),
	)

	conn = op.get_bind()

	for row in conn.execute(old_table.select()):
		conn.execute(new_table.insert().values(id=row.id, seller_id=row.seller_id))

	op.drop_table('old_table')








