"""Adding seller parser id table. Using primary key IDs from the ebay_sellers table is stupid.

Revision ID: fd1f5e2911b3
Revises: d5b8a81a4ec5
Create Date: 2018-06-19 17:00:27.375330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd1f5e2911b3'
down_revision = 'd5b8a81a4ec5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    	'template_parser',
    	sa.Column('template_parser_id', sa.Integer, primary_key=True),
    	sa.Column('file_name_number', sa.Integer, unique=True),
    	sa.Column('parser_file_description', sa.String(140), nullable=True)
    )

    op.add_column('ebay_sellers',
    	sa.Column('template_parser_id', sa.Integer, sa.ForeignKey('template_parser.template_parser_id'))
    )


def downgrade():
    op.drop_column('ebay_sellers', 'template_parser_id')
    op.drop_table('template_parser')
