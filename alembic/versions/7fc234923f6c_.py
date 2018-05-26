"""Create measurement_types table, (rudimentary) items table, and item_measurements link table.

Revision ID: 7fc234923f6c
Revises: b0f2badacd28
Create Date: 2018-05-26 15:29:02.982259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fc234923f6c'
down_revision = 'b0f2badacd28'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'measurement_types',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('type', sa.Text(80), unique=True)
	)

	op.create_table(
		'ebay_items',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('ebay_item_id', sa.Integer, unique=False),  # I'd rather use my own internal ID as primary key
	)

	op.create_table(
		'link_measurement_values_types',
		sa.Column('measurement_id', sa.Integer, sa.ForeignKey('measurement_types.id')),
		sa.Column('ebay_item_id', sa.Integer, sa.ForeignKey('ebay_items.ebay_item_id')),
		sa.Column('measurement_value', sa.Integer),
		sa.UniqueConstraint('measurement_id', 'ebay_item_id', name='uq_item_measurement_type')
	)


def downgrade():
	op.drop_table('link_measurement_values_types')
	op.drop_table('measurement_types')
	op.drop_table('ebay_items')
