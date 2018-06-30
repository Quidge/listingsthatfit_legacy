"""New item measurement tables

Revision ID: ec3ef7d8329b
Revises: 6835b683a2ba
Create Date: 2018-06-30 17:53:17.139997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec3ef7d8329b'
down_revision = '6835b683a2ba'
branch_labels = None
depends_on = None


def upgrade():
	op.drop_table('link_measurement_values_types')
	op.drop_table('measurement_types')

	op.create_table(
		'item_measurement',
		sa.Column('item_measurement_id', sa.Integer, primary_key=True),
		sa.Column('item_measurement_value', sa.Integer, nullable=False),
		sa.Column(
			'measurement_item_category_id',
			sa.Integer,
			sa.ForeignKey('measurement_item_category.measurement_item_category_id'),
			nullable=False),
		sa.Column(
			'measurement_item_type_id',
			sa.Integer,
			sa.ForeignKey('measurement_item_type.measurement_item_type_id'),
			nullable=False),
		sa.Column(
			'ebay_items_id',
			sa.Integer,
			sa.ForeignKey('ebay_items.id'),
			nullable=False),
		sa.UniqueConstraint(
			'measurement_item_category_id',
			'measurement_item_type_id',
			'ebay_items_id')
	)


def downgrade():
	op.drop_table('item_measurements')
	op.create_table(
		'link_measurement_values_types',
		sa.Column('fk_measurement_id', sa.Integer, sa.ForeignKey('measurement_types.id'), nullable=False),
		sa.Column('fk_ebay_items_id', sa.Integer, sa.ForeignKey('ebay_items.id'), nullable=False),
		sa.Column('measurement_value', sa.Integer, nullable=False),
		sa.UniqueConstraint('fk_ebay_items_id', 'fk_measurement_id')
	)

	op.create_table(
		'measurement_types',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('attribute', sa.Text, nullable=False),
		sa.Column('clothing_category', sa.Text, nullable=False),
		sa.UniqueConstraint('attribute', 'clothing_category')
	)














