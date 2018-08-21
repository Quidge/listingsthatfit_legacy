"""remove fk dependency on primary ebay item category id

Revision ID: 9be958d637e7
Revises: a3b2c9699808
Create Date: 2018-08-19 10:46:43.445040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9be958d637e7'
down_revision = 'a3b2c9699808'
branch_labels = None
depends_on = None


def upgrade():
	op.add_column(
		'ebay_items',
		sa.Column(
			'primary_category_number',
			sa.Integer,
			nullable=True)
	)
	op.execute('UPDATE ebay_items SET primary_category_number=ebay_item_category.ebay_item_category_number FROM ebay_item_category WHERE ebay_items.primary_ebay_item_category_id=ebay_item_category.ebay_item_category_id')
	op.alter_column('ebay_items', 'primary_category_number', nullable=False)


def downgrade():
	pass
