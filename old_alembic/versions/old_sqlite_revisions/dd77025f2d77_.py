"""Add in table to hold subscribe-able sellers. Add in link table for many-2-many relationship.

Revision ID: dd77025f2d77
Revises: 75cb7d7cca0a
Create Date: 2018-05-17 12:38:16.699369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd77025f2d77'
down_revision = '75cb7d7cca0a'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'ebay_sellers',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('seller_id', sa.Text(255), nullable=False),
		sa.UniqueConstraint('seller_id', name='uq_seller_id')
	)
	op.create_table(
		'link_user_subscribed_seller',
		sa.Column('seller_id', sa.Integer, sa.ForeignKey('ebay_sellers.id')),
		sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
		sa.UniqueConstraint('seller_id', 'user_id', name='uq_seller_user_subscription')
	)


def downgrade():
	op.drop_table('ebay_sellers')
	op.drop_table('link_user_subscribed_seller')
