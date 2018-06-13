"""first postgres migration


Revision ID: 5b1f9942e785
Revises: 
Create Date: 2018-06-13 11:34:12.070171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b1f9942e785'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'user_accounts',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('email', sa.String(length=64), unique=True),
		sa.Column('password_hash', sa.String(length=255))
	)


def downgrade():
	pass
