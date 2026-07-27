"""add content column

Revision ID: 0b100fc76448
Revises: 8ecfc99924f9
Create Date: 2026-07-27 12:37:03.163351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b100fc76448'
down_revision: Union[str, Sequence[str], None] = '8ecfc99924f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
