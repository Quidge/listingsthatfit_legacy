"""Add ebay sellers table.

Revision ID: 7b295fae73b4
Revises: 04188bea6ae3
Create Date: 2018-06-13 13:11:24.549477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b295fae73b4'
down_revision = '04188bea6ae3'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'ebay_sellers',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('ebay_seller_id', sa.Text, nullable=False, unique=True),
		sa.Column('all_items_url', sa.Text),
		sa.Column('store_url', sa.Text)
	)


def downgrade():
    pass
