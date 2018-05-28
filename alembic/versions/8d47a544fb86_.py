"""Fleshed out ebay_items table with more columns.

Revision ID: 8d47a544fb86
Revises: 7fc234923f6c
Create Date: 2018-05-28 11:35:00.457606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d47a544fb86'
down_revision = '7fc234923f6c'
branch_labels = None
depends_on = None


def upgrade():
	op.add_column('ebay_items', sa.Column('end_date', sa.DateTime))
	op.add_column('ebay_items', sa.Column('last_access_date', sa.DateTime))
	op.add_column('ebay_items', sa.Column('ebay_title', sa.Text(80)))
	op.add_column('ebay_items', sa.Column('ebay_primary_category_id', sa.Integer))
	op.add_column('ebay_items', sa.Column('current_price', sa.Integer))
	op.add_column('ebay_items', sa.Column('ebay_url', sa.Text()))
	op.add_column('ebay_items', sa.Column('ebay_affiliate_url', sa.Text()))


def downgrade():
	with op.batch_alter_table('ebay_items') as batch_op:
		batch_op.drop_column('end_date')
		batch_op.drop_column('last_access_date')
		batch_op.drop_column('ebay_title')
		batch_op.drop_column('ebay_primary_category_id')
		batch_op.drop_column('current_price')
		batch_op.drop_column('ebay_url')
		batch_op.drop_column('ebay_affiliate_url')
