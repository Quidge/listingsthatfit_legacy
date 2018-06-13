"""Divided measurement_types.type_name into two columns: attribute and clothing_category.

Revision ID: a9afa8886c30
Revises: 8d47a544fb86
Create Date: 2018-05-28 15:18:53.592315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9afa8886c30'
down_revision = '8d47a544fb86'
branch_labels = None
depends_on = None


def upgrade():
	op.drop_table('measurement_types')
	op.create_table(
		'measurement_types',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('attribute', sa.Text()),
		sa.Column('clothing_category', sa.Text()),
		sa.UniqueConstraint(
			'attribute',
			'clothing_category',
			name='uq_attribute_cat_combination'
		)
	)


def downgrade():
	op.drop_table('measurement_types')
	op.create_table(
		'measurement_types',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('type_name', sa.Text(), unique=True)
	)
