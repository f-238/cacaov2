from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select

from app.database import SyncSessionLocal
from app.models.alert import AlertSeverity, DeviceAlert
from app.models.device import Device
from app.models.sensor_reading import SensorReading
from app.models.user import User, UserRole
from app.utils.security import get_password_hash


ADMIN_EMAIL = "admin@cacaomonitor.local"
USER_EMAIL = "user@cacaomonitor.local"
DEVICE_SERIAL = "CACAO-DEV-0001"


def get_or_create_user(
    db,
    *,
    full_name: str,
    email: str,
    password: str,
    role: UserRole,
) -> User:
    user = db.scalar(select(User).where(User.email == email))
    hashed_password = get_password_hash(password)

    if user is None:
        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hashed_password,
            role=role,
            is_active=True,
        )
        db.add(user)
        db.flush()
        return user

    user.full_name = full_name
    user.hashed_password = hashed_password
    user.role = role
    user.is_active = True
    db.flush()
    return user


def get_or_create_device(db, *, user_id: int) -> Device:
    device = db.scalar(select(Device).where(Device.device_serial == DEVICE_SERIAL))
    last_seen = datetime.now(timezone.utc)

    if device is None:
        device = Device(
            device_name="Cacao Dryer Main Unit",
            device_serial=DEVICE_SERIAL,
            user_id=user_id,
            last_seen=last_seen,
            is_online=True,
            firmware_version="v1.2.0",
        )
        db.add(device)
        db.flush()
        return device

    device.device_name = "Cacao Dryer Main Unit"
    device.user_id = user_id
    device.last_seen = last_seen
    device.is_online = True
    device.firmware_version = "v1.2.0"
    db.flush()
    return device


def reseed_sensor_readings(db, *, device_id: int) -> int:
    db.execute(delete(SensorReading).where(SensorReading.device_id == device_id))

    base_time = datetime.now(timezone.utc) - timedelta(hours=23)
    readings: list[SensorReading] = []

    for index in range(24):
        timestamp = base_time + timedelta(hours=index)
        readings.append(
            SensorReading(
                device_id=device_id,
                timestamp=timestamp,
                temperature=46.5 + (index * 0.28) + ((index % 4) * 0.35),
                moisture=17.8 - (index * 0.32) + ((index % 3) * 0.08),
                ambient_temp=29.2 + (index * 0.14) + ((index % 5) * 0.1),
            )
        )

    db.add_all(readings)
    db.flush()
    return len(readings)


def reseed_alerts(db, *, device_id: int, user_id: int) -> int:
    db.execute(delete(DeviceAlert).where(DeviceAlert.device_id == device_id))

    now = datetime.now(timezone.utc)
    alerts = [
        DeviceAlert(
            device_id=device_id,
            user_id=user_id,
            type="system",
            severity=AlertSeverity.INFO,
            message="Device connected and operating within normal thresholds.",
            resolved=False,
            created_at=now - timedelta(hours=8),
        ),
        DeviceAlert(
            device_id=device_id,
            user_id=user_id,
            type="moisture",
            severity=AlertSeverity.WARNING,
            message="Moisture level is above the target drying range.",
            resolved=False,
            created_at=now - timedelta(hours=4),
        ),
        DeviceAlert(
            device_id=device_id,
            user_id=user_id,
            type="temperature",
            severity=AlertSeverity.CRITICAL,
            message="Temperature exceeded the critical safety threshold.",
            resolved=False,
            created_at=now - timedelta(hours=1),
        ),
    ]

    db.add_all(alerts)
    db.flush()
    return len(alerts)


def main() -> None:
    with SyncSessionLocal() as db:
        admin_user = get_or_create_user(
            db,
            full_name="System Administrator",
            email=ADMIN_EMAIL,
            password="admin123",
            role=UserRole.ADMIN,
        )
        normal_user = get_or_create_user(
            db,
            full_name="Normal User",
            email=USER_EMAIL,
            password="user123",
            role=UserRole.USER,
        )
        device = get_or_create_device(db, user_id=normal_user.id)
        reading_count = reseed_sensor_readings(db, device_id=device.id)
        alert_count = reseed_alerts(db, device_id=device.id, user_id=normal_user.id)
        db.commit()

    print("Seed complete.")
    print(f"Admin user: {ADMIN_EMAIL} / admin123")
    print(f"Normal user: {USER_EMAIL} / user123")
    print(f"Device serial: {DEVICE_SERIAL}")
    print(f"Sensor readings inserted: {reading_count}")
    print(f"Alerts inserted: {alert_count}")


if __name__ == "__main__":
    main()
