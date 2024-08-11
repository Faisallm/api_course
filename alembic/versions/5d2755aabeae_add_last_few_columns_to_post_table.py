"""add last few columns to post table

Revision ID: 5d2755aabeae
Revises: d6e18ad0ea21
Create Date: 2024-08-11 03:01:32.547674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d2755aabeae'
down_revision: Union[str, None] = 'd6e18ad0ea21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published",
        sa.Boolean(), nullable=False, server_default="TRUE")),
    op.add_column("posts", sa.Column("created_at",
                  sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_column('posts', "published")
    op.drop_column('posts', "created_at")
    pass
