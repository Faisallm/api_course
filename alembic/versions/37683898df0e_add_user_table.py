"""Add user Table

Revision ID: 37683898df0e
Revises: 22911ae7b510
Create Date: 2024-08-11 02:42:39.634002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37683898df0e'
down_revision: Union[str, None] = '22911ae7b510'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
        )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
