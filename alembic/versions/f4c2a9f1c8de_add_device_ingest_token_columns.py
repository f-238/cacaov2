"""add device ingest token columns

Revision ID: f4c2a9f1c8de
Revises: 2b569263f19d
Create Date: 2026-04-09 22:45:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f4c2a9f1c8de"
down_revision = "2b569263f19d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("devices", sa.Column("ingest_token_hash", sa.String(length=64), nullable=True))
    op.add_column("devices", sa.Column("ingest_token_created_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index(
        op.f("ix_devices_ingest_token_hash"),
        "devices",
        ["ingest_token_hash"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_devices_ingest_token_hash"), table_name="devices")
    op.drop_column("devices", "ingest_token_created_at")
    op.drop_column("devices", "ingest_token_hash")
