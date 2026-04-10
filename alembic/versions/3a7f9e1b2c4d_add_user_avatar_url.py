"""add user avatar url

Revision ID: 3a7f9e1b2c4d
Revises: 8d9c1b2a4e7f
Create Date: 2026-04-09 23:35:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3a7f9e1b2c4d"
down_revision = "8d9c1b2a4e7f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("avatar_url", sa.String(length=512), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "avatar_url")
