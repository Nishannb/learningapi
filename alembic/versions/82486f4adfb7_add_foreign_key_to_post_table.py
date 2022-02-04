"""add foreign key to post table

Revision ID: 82486f4adfb7
Revises: 0d05e534a32d
Create Date: 2022-02-03 21:24:04.063114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82486f4adfb7'
down_revision = '0d05e534a32d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table='users', 
                            local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass
    


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts") 
    op.drop_column('posts', "owner_id")
    pass