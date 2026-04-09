from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.sensor_reading import SensorReading
from app.models.user import User
from app.schemas.sensor_reading import SensorReadingSummary
from app.services.devices import get_device_for_user
from app.utils.export import build_dataframe, export_dataframe


def list_readings_for_device(db: Session, user: User, device_id: int) -> list[SensorReading]:
    get_device_for_user(db, user, device_id)
    return (
        db.query(SensorReading)
        .filter(SensorReading.device_id == device_id)
        .order_by(SensorReading.timestamp.desc())
        .all()
    )


def get_latest_reading_for_device(db: Session, user: User, device_id: int) -> SensorReading:
    get_device_for_user(db, user, device_id)
    reading = (
        db.query(SensorReading)
        .filter(SensorReading.device_id == device_id)
        .order_by(SensorReading.timestamp.desc())
        .first()
    )

    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sensor readings found for this device.",
        )

    return reading


def get_readings_summary_for_device(db: Session, user: User, device_id: int) -> SensorReadingSummary:
    get_device_for_user(db, user, device_id)
    aggregates = (
        db.query(
            func.count(SensorReading.id),
            func.avg(SensorReading.temperature),
            func.min(SensorReading.temperature),
            func.max(SensorReading.temperature),
            func.avg(SensorReading.moisture),
            func.min(SensorReading.moisture),
            func.max(SensorReading.moisture),
            func.avg(SensorReading.ambient_temp),
            func.min(SensorReading.ambient_temp),
            func.max(SensorReading.ambient_temp),
        )
        .filter(SensorReading.device_id == device_id)
        .one()
    )

    return SensorReadingSummary(
        count=aggregates[0] or 0,
        avg_temperature=_to_float(aggregates[1]),
        min_temperature=_to_float(aggregates[2]),
        max_temperature=_to_float(aggregates[3]),
        avg_moisture=_to_float(aggregates[4]),
        min_moisture=_to_float(aggregates[5]),
        max_moisture=_to_float(aggregates[6]),
        avg_ambient_temp=_to_float(aggregates[7]),
        min_ambient_temp=_to_float(aggregates[8]),
        max_ambient_temp=_to_float(aggregates[9]),
    )


def export_readings_for_device(db: Session, user: User, device_id: int, export_format: str) -> tuple[bytes, str, str]:
    readings = list_readings_for_device(db, user, device_id)
    if not readings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sensor readings found for this device.",
        )

    frame = build_dataframe(
        [
            {
                "id": reading.id,
                "device_id": reading.device_id,
                "timestamp": reading.timestamp.isoformat(),
                "temperature": reading.temperature,
                "moisture": reading.moisture,
                "ambient_temp": reading.ambient_temp,
            }
            for reading in readings
        ]
    )

    return export_dataframe(frame, f"device-{device_id}-readings", export_format)


def _to_float(value: object) -> float | None:
    if value is None:
        return None
    return round(float(value), 4)
