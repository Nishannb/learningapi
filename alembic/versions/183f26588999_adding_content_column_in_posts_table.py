"""Adding content column in posts table

Revision ID: 183f26588999
Revises: 1e7c1a370162
Create Date: 2022-02-03 21:08:53.167818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '183f26588999'
down_revision = '1e7c1a370162'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
    pass
