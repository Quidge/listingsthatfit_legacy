"""Add unique constraints to size key tables. (>1 entry for the numerical size shouldn't be possible

Revision ID: cb27d05c41b8
Revises: 929822e572b8
Create Date: 2018-04-29 14:00:17.072224

"""
from alembic import op
from app.models import SizeKeyShirtDressNeck
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb27d05c41b8'
down_revision = '929822e572b8'
branch_labels = None
depends_on = None


'''def upgrade2():
	op.rename_table('size_key_shirt_dress_neck', 'old_neck')
	new_table = op.create_table(
		'size_key_shirt_dress_neck',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer),
		sa.UniqueConstraint('size', name='uq_size')
	)
'''


def upgrade():
	'''new_table = op.create_table(
		'temp',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('size', sa.Integer),
		sa.UniqueConstraint('size', name='uq_size')
	)

	records = SizeKeyShirtDressNeck.__table__

	op.bulk_insert(new_table, )'''
	pass

def downgrade():
	#op.drop_constraint(
	#	'uq_size_key',
	#	'size_key_shirt_dress_sleeve'
	#)
	pass
