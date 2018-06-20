"""change ebay items id col from integer to BigInteger

Revision ID: d5b8a81a4ec5
Revises: a5e694d7897e
Create Date: 2018-06-16 09:14:36.581497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5b8a81a4ec5'
down_revision = 'a5e694d7897e'
branch_labels = None
depends_on = None


def upgrade():
	op.alter_column(
		'ebay_items', 'ebay_item_id',
		type_=sa.BigInteger, existing_type=sa.Integer,
	)


def downgrade():
	# 'What if there are already BigInt data present? What do I do? Cry.'
	op.alter_column(
		'ebay_items', 'ebay_item_id',
		type_=sa.Integer, existing_type=sa.BigInteger,
	)
