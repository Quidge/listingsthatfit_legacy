"""shirt size key user link tables

Revision ID: 46e65a12a27a
Revises: 94adc7884db4
Create Date: 2018-06-13 12:21:41.096829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46e65a12a27a'
down_revision = '94adc7884db4'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'link_user_accounts_size_shirt_dress_sleeve',
		sa.Column('size_id', sa.Integer, sa.ForeignKey('size_key_shirt_dress_sleeve.id'), nullable=False),
		sa.Column('user_accounts_id', sa.Integer, sa.ForeignKey('user_accounts.id'), nullable=False),
		sa.UniqueConstraint('size_id', 'user_accounts_id')
	)


def downgrade():
    pass
