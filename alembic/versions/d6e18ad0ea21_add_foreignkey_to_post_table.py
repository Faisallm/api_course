"""Add foreignkey to post table

Revision ID: d6e18ad0ea21
Revises: 37683898df0e
Create Date: 2024-08-11 02:52:34.673905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6e18ad0ea21'
down_revision: Union[str, None] = '37683898df0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add owner_id column.
    op.add_column("posts", sa.Column("owner_id", sa.Integer))
    # create user constraint.
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users",
                          local_cols=["owner_id"], remote_cols=["id"],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
