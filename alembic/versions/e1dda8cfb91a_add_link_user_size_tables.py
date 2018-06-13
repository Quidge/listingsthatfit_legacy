"""Add size_key_shirt_dress_sleeve

Revision ID: e1dda8cfb91a
Revises: 5b1f9942e785
Create Date: 2018-06-13 11:41:38.549900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1dda8cfb91a'
down_revision = '5b1f9942e785'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'size_key_shirt_dress_sleeve',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer, unique=True)
	)


def downgrade():
    pass
