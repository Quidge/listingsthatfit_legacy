"""Link ebay_items and ebay_item_category. Remove old col and replace with FK link.

Revision ID: bc02fc84ff70
Revises: ec3ef7d8329b
Create Date: 2018-07-01 14:28:30.345302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc02fc84ff70'
down_revision = 'ec3ef7d8329b'
branch_labels = None
depends_on = None


def upgrade():
	op.drop_column('ebay_items', 'ebay_primary_category')
	op.add_column(
		'ebay_items',
		sa.Column(
			'primary_ebay_item_category_id',
			sa.Integer,
			sa.ForeignKey('ebay_item_category.ebay_item_category_id')
		)
	)


def downgrade():
	op.drop_column('ebay_items', 'primary_ebay_item_category_id')
	op.add_column(
		'ebay_items',
		sa.Column(
			'ebay_primary_category',
			sa.Integer)
	)
