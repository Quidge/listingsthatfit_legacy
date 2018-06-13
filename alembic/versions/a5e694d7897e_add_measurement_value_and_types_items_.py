"""Add measurement value and types + items link table

Revision ID: a5e694d7897e
Revises: 40f17d77fc72
Create Date: 2018-06-13 14:00:42.679235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5e694d7897e'
down_revision = '40f17d77fc72'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'link_measurement_values_types',
		sa.Column('fk_measurement_id', sa.Integer, sa.ForeignKey('measurement_types.id'), nullable=False),
		sa.Column('fk_ebay_items_id', sa.Integer, sa.ForeignKey('ebay_items.id'), nullable=False),
		sa.Column('measurement_value', sa.Integer, nullable=False),
		sa.UniqueConstraint('fk_ebay_items_id', 'fk_measurement_id')
	)


def downgrade():
	op.drop_table('link_measurement_values_types')
