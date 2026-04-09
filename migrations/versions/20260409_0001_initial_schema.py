"""initial schema

Revision ID: 20260409_0001
Revises: None
Create Date: 2026-04-09 16:30:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260409_0001"
down_revision = None
branch_labels = None
depends_on = None


user_role_enum = sa.Enum("user", "admin", name="user_role")
alert_severity_enum = sa.Enum("info", "warning", "critical", name="alert_severity")


def upgrade() -> None:
    bind = op.get_bind()
    user_role_enum.create(bind, checkfirst=True)
    alert_severity_enum.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role_enum, nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("device_name", sa.String(length=255), nullable=False),
        sa.Column("device_serial", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_online", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("firmware_version", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index(op.f("ix_devices_id"), "devices", ["id"], unique=False)
    op.create_index(op.f("ix_devices_device_serial"), "devices", ["device_serial"], unique=True)
    op.create_index(op.f("ix_devices_user_id"), "devices", ["user_id"], unique=False)

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("token", sa.String(length=512), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index(op.f("ix_refresh_tokens_id"), "refresh_tokens", ["id"], unique=False)
    op.create_index(op.f("ix_refresh_tokens_token"), "refresh_tokens", ["token"], unique=True)

    op.create_table(
        "device_alerts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=100), nullable=False),
        sa.Column("severity", alert_severity_enum, nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("resolved", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index(op.f("ix_device_alerts_id"), "device_alerts", ["id"], unique=False)
    op.create_index(op.f("ix_device_alerts_device_id"), "device_alerts", ["device_id"], unique=False)
    op.create_index(op.f("ix_device_alerts_user_id"), "device_alerts", ["user_id"], unique=False)

    op.create_table(
        "sensor_readings",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("moisture", sa.Float(), nullable=False),
        sa.Column("ambient_temp", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="CASCADE"),
    )
    op.create_index(op.f("ix_sensor_readings_id"), "sensor_readings", ["id"], unique=False)
    op.create_index(op.f("ix_sensor_readings_device_id"), "sensor_readings", ["device_id"], unique=False)
    op.create_index(op.f("ix_sensor_readings_timestamp"), "sensor_readings", ["timestamp"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_index(op.f("ix_sensor_readings_timestamp"), table_name="sensor_readings")
    op.drop_index(op.f("ix_sensor_readings_device_id"), table_name="sensor_readings")
    op.drop_index(op.f("ix_sensor_readings_id"), table_name="sensor_readings")
    op.drop_table("sensor_readings")

    op.drop_index(op.f("ix_device_alerts_user_id"), table_name="device_alerts")
    op.drop_index(op.f("ix_device_alerts_device_id"), table_name="device_alerts")
    op.drop_index(op.f("ix_device_alerts_id"), table_name="device_alerts")
    op.drop_table("device_alerts")

    op.drop_index(op.f("ix_refresh_tokens_token"), table_name="refresh_tokens")
    op.drop_index(op.f("ix_refresh_tokens_id"), table_name="refresh_tokens")
    op.drop_table("refresh_tokens")

    op.drop_index(op.f("ix_devices_user_id"), table_name="devices")
    op.drop_index(op.f("ix_devices_device_serial"), table_name="devices")
    op.drop_index(op.f("ix_devices_id"), table_name="devices")
    op.drop_table("devices")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")

    alert_severity_enum.drop(bind, checkfirst=True)
    user_role_enum.drop(bind, checkfirst=True)
