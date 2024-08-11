"""Add content column to post table

Revision ID: 22911ae7b510
Revises: c8376a785995
Create Date: 2024-08-11 02:37:08.566974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22911ae7b510'
down_revision: Union[str, None] = 'c8376a785995'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
