"""User measurement tables. Also ebay item categories table.

Revision ID: 6835b683a2ba
Revises: fd1f5e2911b3
Create Date: 2018-06-29 12:00:07.343147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6835b683a2ba'
down_revision = 'fd1f5e2911b3'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'ebay_item_category',
		sa.Column('ebay_item_category_id', sa.Integer, primary_key=True),
		sa.Column('ebay_item_category_number', sa.Integer, unique=True, nullable=False),
		sa.Column('ebay_item_category_name', sa.Text))
	op.create_table(
		'user_measurement_item_category',
		sa.Column('user_measurement_item_category_id', sa.Integer, primary_key=True),
		sa.Column('user_measurement_item_category_name', sa.Text, unique=True, nullable=False))
	op.create_table(
		'user_measurement_item_type',
		sa.Column('user_measurement_item_type_id', sa.Integer, primary_key=True),
		sa.Column('user_measurement_item_type_name', sa.Text, unique=True, nullable=False))
	op.create_table(
		'user_measurement_preference',
		sa.Column('user_measurement_preference_id', sa.Integer, primary_key=True),
		sa.Column('measurement_range_start_inch_factor', sa.Integer, nullable=False),
		sa.Column('measurement_range_end_inch_factor', sa.Integer, nullable=False),
		sa.Column(
			'ebay_item_category_id',
			sa.Integer,
			sa.ForeignKey('ebay_item_category.ebay_item_category_id'),
			nullable=False),
		sa.Column(
			'user_measurement_item_category_id',
			sa.Integer,
			sa.ForeignKey('user_measurement_item_category.user_measurement_item_category_id'),
			nullable=False),
		sa.Column(
			'user_measurement_item_type_id',
			sa.Integer,
			sa.ForeignKey('user_measurement_item_type.user_measurement_item_type_id'),
			nullable=False),
		sa.Column(
			'user_accounts_id',
			sa.Integer,
			sa.ForeignKey('user_accounts.id'),
			nullable=False)
	)
	op.create_unique_constraint(
		'uq_table_user_measurement_ebay_item_category_id_item_category_id_user_measurement_item_type_id_user_accounts_id',
		'user_measurement_preference',
		[
			'ebay_item_category_id',
			'user_measurement_item_category_id',
			'user_measurement_item_type_id',
			'user_accounts_id'
		]
	)


def downgrade():
	op.drop_table('user_measurement_preference')
	op.drop_table('user_measurement_item_category')
	op.drop_table('user_measurement_item_type')
	op.drop_table('ebay_item_category')





