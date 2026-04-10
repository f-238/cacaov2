"""add user settings table

Revision ID: 8d9c1b2a4e7f
Revises: f4c2a9f1c8de
Create Date: 2026-04-09 23:05:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8d9c1b2a4e7f"
down_revision = "f4c2a9f1c8de"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("theme_mode", sa.String(length=10), server_default=sa.text("'system'"), nullable=False),
        sa.Column("font_size", sa.String(length=10), server_default=sa.text("'medium'"), nullable=False),
        sa.Column("primary_color", sa.String(length=7), server_default=sa.text("'#1f2937'"), nullable=False),
        sa.Column("secondary_color", sa.String(length=7), server_default=sa.text("'#526075'"), nullable=False),
        sa.Column("accent_color", sa.String(length=7), server_default=sa.text("'#f3a6ba'"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "theme_mode IN ('light', 'dark', 'system')",
            name="ck_user_settings_theme_mode",
        ),
        sa.CheckConstraint(
            "font_size IN ('small', 'medium', 'large')",
            name="ck_user_settings_font_size",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(op.f("ix_user_settings_id"), "user_settings", ["id"], unique=False)
    op.create_index(op.f("ix_user_settings_user_id"), "user_settings", ["user_id"], unique=True)

    op.execute(
        """
        INSERT INTO user_settings (user_id)
        SELECT users.id
        FROM users
        LEFT JOIN user_settings ON user_settings.user_id = users.id
        WHERE user_settings.user_id IS NULL
        """
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_user_settings_user_id"), table_name="user_settings")
    op.drop_index(op.f("ix_user_settings_id"), table_name="user_settings")
    op.drop_table("user_settings")
