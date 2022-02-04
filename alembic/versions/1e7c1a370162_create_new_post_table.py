"""Create new post table

Revision ID: 1e7c1a370162
Revises: 
Create Date: 2022-02-03 20:47:07.201380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e7c1a370162'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    


def downgrade():
    op.drop_table('posts')
    
