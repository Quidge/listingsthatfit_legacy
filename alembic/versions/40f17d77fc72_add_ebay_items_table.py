"""Add ebay items table

Revision ID: 40f17d77fc72
Revises: 502a69e3780b
Create Date: 2018-06-13 13:34:09.390308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40f17d77fc72'
down_revision = '502a69e3780b'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'ebay_items',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('ebay_item_id', sa.Integer, nullable=False),
		sa.Column('end_date', sa.DateTime, nullable=False),
		sa.Column('last_access_date', sa.DateTime, nullable=False),
		sa.Column('ebay_title', sa.Text, nullable=False),
		sa.Column('ebay_primary_category', sa.Integer),
		sa.Column('current_price', sa.Integer),
		sa.Column('ebay_url', sa.Text),
		sa.Column('ebay_affiliate_url', sa.Text),
		sa.Column('internal_seller_id', sa.Integer, sa.ForeignKey('ebay_sellers.id'), nullable=False)
	)


def downgrade():
	op.drop_table('ebay_items')
