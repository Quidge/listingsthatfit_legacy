"""create clothing_category table and link to ebay_items

Revision ID: a3b2c9699808
Revises: bc02fc84ff70
Create Date: 2018-08-17 17:51:08.706879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3b2c9699808'
down_revision = 'bc02fc84ff70'
branch_labels = None
depends_on = None


def upgrade():
		op.create_table(
			'clothing_category',
			sa.Column('clothing_category_id', sa.Integer, primary_key=True),
			sa.Column('clothing_category_name', sa.Text, unique=True, nullable=False)
		)
		op.add_column(
			'ebay_items',
			sa.Column(
				'clothing_category_id', sa.Integer,
				sa.ForeignKey('clothing_category.clothing_category_id')))


def downgrade():
	op.drop_column('ebay_items', 'clothing_category_id')
	op.drop_table('clothing_category')
