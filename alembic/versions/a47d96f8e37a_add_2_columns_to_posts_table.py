"""add 2 columns to posts table

Revision ID: a47d96f8e37a
Revises: 93d06ee1c0a5
Create Date: 2026-07-27 13:30:09.111530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a47d96f8e37a'
down_revision: Union[str, Sequence[str], None] = '93d06ee1c0a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
        server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
