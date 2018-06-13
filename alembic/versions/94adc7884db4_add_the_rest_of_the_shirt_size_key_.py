"""Add the rest of the shirt size key tables

Revision ID: 94adc7884db4
Revises: e1dda8cfb91a
Create Date: 2018-06-13 12:04:15.018499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94adc7884db4'
down_revision = 'e1dda8cfb91a'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'size_key_shirt_dress_neck',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer, unique=True)
	)
	op.create_table(
		'size_key_shirt_casual',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Text, unique=True)
	)


def downgrade():
	pass
