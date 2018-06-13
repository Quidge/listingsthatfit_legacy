"""Add the rest of the shirt size key user link tables

Revision ID: 04188bea6ae3
Revises: 46e65a12a27a
Create Date: 2018-06-13 13:01:37.547991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04188bea6ae3'
down_revision = '46e65a12a27a'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'link_user_accounts_size_shirt_dress_neck',
		sa.Column('size_id', sa.Integer, sa.ForeignKey('size_key_shirt_dress_neck.id'), nullable=False),
		sa.Column('user_accounts_id', sa.Integer, sa.ForeignKey('user_accounts.id'), nullable=False),
		sa.UniqueConstraint('size_id', 'user_accounts_id')
	)
	op.create_table(
		'link_user_accounts_size_shirt_casual',
		sa.Column('size_id', sa.Integer, sa.ForeignKey('size_key_shirt_casual.id'), nullable=False),
		sa.Column('user_accounts_id', sa.Integer, sa.ForeignKey('user_accounts.id'), nullable=False),
		sa.UniqueConstraint('size_id', 'user_accounts_id')
	)


def downgrade():
    pass
