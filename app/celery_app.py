from datetime import UTC, datetime
import random

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import select

from app.config import get_settings
from app.database import SyncSessionLocal
from app.models.alert import AlertSeverity, DeviceAlert
from app.models.device import Device
from app.models.sensor_reading import SensorReading


settings = get_settings()

celery_app = Celery(
    "cacao_monitor",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "generate-demo-sensor-data": {
            "task": "app.celery_app.generate_fake_sensor_data_for_all_devices",
            "schedule": 120.0,
        },
        "check-demo-alerts": {
            "task": "app.celery_app.check_alerts",
            "schedule": crontab(minute="*/1"),
        },
    },
)


@celery_app.task(name="app.celery_app.ping")
def ping_task() -> str:
    return "pong"


@celery_app.task(name="app.celery_app.generate_fake_sensor_data")
def generate_fake_sensor_data(device_id: int) -> dict[str, float | int | str]:
    with SyncSessionLocal() as db:
        device = db.get(Device, device_id)
        if not device:
            raise ValueError(f"Device {device_id} was not found.")

        reading = _insert_fake_sensor_reading(db, device)
        db.commit()
        db.refresh(reading)

        return {
            "reading_id": reading.id,
            "device_id": device.id,
            "timestamp": reading.timestamp.isoformat(),
            "temperature": reading.temperature,
            "moisture": reading.moisture,
            "ambient_temp": reading.ambient_temp,
        }


@celery_app.task(name="app.celery_app.generate_fake_sensor_data_for_all_devices")
def generate_fake_sensor_data_for_all_devices() -> dict[str, int]:
    created_count = 0

    with SyncSessionLocal() as db:
        devices = db.execute(select(Device)).scalars().all()

        for device in devices:
            _insert_fake_sensor_reading(db, device)
            created_count += 1

        db.commit()

    return {"generated_readings": created_count}


@celery_app.task(name="app.celery_app.check_alerts")
def check_alerts() -> dict[str, int]:
    thresholds = {
        "critical_temperature": 56.0,
        "warning_temperature": 52.0,
        "critical_moisture": 17.0,
        "warning_moisture": 15.0,
        "critical_ambient_temp": 35.0,
        "warning_ambient_temp": 33.0,
    }

    created_count = 0

    with SyncSessionLocal() as db:
        devices = db.execute(select(Device)).scalars().all()

        for device in devices:
            latest_reading = (
                db.execute(
                    select(SensorReading)
                    .where(SensorReading.device_id == device.id)
                    .order_by(SensorReading.timestamp.desc())
                )
                .scalars()
                .first()
            )

            if not latest_reading:
                continue

            alert_payloads = []

            if latest_reading.temperature >= thresholds["critical_temperature"]:
                alert_payloads.append(
                    _build_alert(
                        device=device,
                        alert_type="Temperature",
                        severity=AlertSeverity.CRITICAL,
                        message=(
                            f"Critical temperature detected at {latest_reading.temperature:.2f} C."
                        ),
                    )
                )
            elif latest_reading.temperature >= thresholds["warning_temperature"]:
                alert_payloads.append(
                    _build_alert(
                        device=device,
                        alert_type="Temperature",
                        severity=AlertSeverity.WARNING,
                        message=(
                            f"High temperature warning at {latest_reading.temperature:.2f} C."
                        ),
                    )
                )

            if latest_reading.moisture >= thresholds["critical_moisture"]:
                alert_payloads.append(
                    _build_alert(
                        device=device,
                        alert_type="Moisture",
                        severity=AlertSeverity.CRITICAL,
                        message=(
                            f"Critical moisture level detected at {latest_reading.moisture:.2f}%."
                        ),
                    )
                )
            elif latest_reading.moisture >= thresholds["warning_moisture"]:
                alert_payloads.append(
                    _build_alert(
                        device=device,
                        alert_type="Moisture",
                        severity=AlertSeverity.WARNING,
                        message=(
                            f"Moisture warning detected at {latest_reading.moisture:.2f}%."
                        ),
                    )
                )

            if latest_reading.ambient_temp >= thresholds["critical_ambient_temp"]:
                alert_payloads.append(
                    _build_alert(
                        device=device,
                        alert_type="Ambient Temperature",
                        severity=AlertSeverity.CRITICAL,
                        message=(
                            f"Critical ambient temperature at {latest_reading.ambient_temp:.2f} C."
                        ),
                    )
                )
            elif latest_reading.ambient_temp >= thresholds["warning_ambient_temp"]:
                alert_payloads.append(
                    _build_alert(
                        device=device,
                        alert_type="Ambient Temperature",
                        severity=AlertSeverity.WARNING,
                        message=(
                            f"Ambient temperature warning at {latest_reading.ambient_temp:.2f} C."
                        ),
                    )
                )

            for payload in alert_payloads:
                already_exists = (
                    db.execute(
                        select(DeviceAlert).where(
                            DeviceAlert.device_id == device.id,
                            DeviceAlert.type == payload["type"],
                            DeviceAlert.severity == payload["severity"],
                            DeviceAlert.message == payload["message"],
                            DeviceAlert.resolved.is_(False),
                        )
                    )
                    .scalars()
                    .first()
                )

                if already_exists:
                    continue

                db.add(DeviceAlert(**payload))
                created_count += 1

        db.commit()

    return {"created_alerts": created_count}


def _insert_fake_sensor_reading(db, device: Device) -> SensorReading:
    temperature = round(random.uniform(42.0, 58.0), 2)
    moisture = round(random.uniform(8.0, 18.0), 2)
    ambient_temp = round(random.uniform(28.0, 36.0), 2)
    captured_at = datetime.now(UTC)

    reading = SensorReading(
        device_id=device.id,
        timestamp=captured_at,
        temperature=temperature,
        moisture=moisture,
        ambient_temp=ambient_temp,
    )
    device.last_seen = captured_at
    device.is_online = True

    db.add(reading)
    db.add(device)
    return reading


def _build_alert(
    *,
    device: Device,
    alert_type: str,
    severity: AlertSeverity,
    message: str,
) -> dict[str, int | str | bool | AlertSeverity]:
    return {
        "device_id": device.id,
        "user_id": device.user_id,
        "type": alert_type,
        "severity": severity,
        "message": message,
        "resolved": False,
    }


__all__ = [
    "celery_app",
    "ping_task",
    "generate_fake_sensor_data",
    "generate_fake_sensor_data_for_all_devices",
    "check_alerts",
]
