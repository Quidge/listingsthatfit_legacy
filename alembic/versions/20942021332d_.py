"""Added seller_id FK to ebay_items table

Revision ID: 20942021332d
Revises: a9afa8886c30
Create Date: 2018-05-29 13:55:40.767783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20942021332d'
down_revision = 'a9afa8886c30'
branch_labels = None
depends_on = None


def upgrade():
	with op.batch_alter_table('ebay_items') as batch_op:
		batch_op.add_column(
			sa.Column(
				'seller_id',
				sa.Integer,
				sa.ForeignKey('ebay_sellers.id', name='ebay_sellers_fk')
			)
		)


def downgrade():
	with op.batch_alter_table('ebay_items') as batch_op:
		batch_op.drop_column('seller_id')
