"""Add measurement types.

Revision ID: 502a69e3780b
Revises: e8a7197b8344
Create Date: 2018-06-13 13:25:59.131285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '502a69e3780b'
down_revision = 'e8a7197b8344'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'measurement_types',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('attribute', sa.Text, nullable=False),
		sa.Column('clothing_category', sa.Text, nullable=False),
		sa.UniqueConstraint('attribute', 'clothing_category')
	)


def downgrade():
	op.drop_table('measurement_types')
