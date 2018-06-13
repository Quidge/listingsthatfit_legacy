"""Add ebay sellers and users association table

Revision ID: e8a7197b8344
Revises: 7b295fae73b4
Create Date: 2018-06-13 13:18:34.614067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8a7197b8344'
down_revision = '7b295fae73b4'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'link_user_accounts_subscribed_seller',
		sa.Column('seller_id', sa.Integer, sa.ForeignKey('ebay_sellers.id'), nullable=False),
		sa.Column('user_accounts_id', sa.Integer, sa.ForeignKey('user_accounts.id'), nullable=False),
		sa.UniqueConstraint('seller_id', 'user_accounts_id')
	)


def downgrade():
    pass
