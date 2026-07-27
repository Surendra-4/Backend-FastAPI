"""add fkey to posts

Revision ID: 93d06ee1c0a5
Revises: 843ff92ebc77
Create Date: 2026-07-27 13:19:39.911445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93d06ee1c0a5'
down_revision: Union[str, Sequence[str], None] = '843ff92ebc77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users',
                        local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
