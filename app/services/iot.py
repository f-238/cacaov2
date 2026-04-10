from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.sensor_reading import SensorReading
from app.schemas.iot import IoTReadingIngestRequest
from app.utils.device_tokens import hash_device_token


def ingest_sensor_reading(
    db: Session,
    device_token: str,
    payload: IoTReadingIngestRequest,
) -> SensorReading:
    token_hash = hash_device_token(device_token)
    device = db.query(Device).filter(Device.ingest_token_hash == token_hash).first()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid device token.",
        )

    if device.device_serial != payload.device_serial:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Device serial does not match token identity.",
        )

    captured_at = payload.timestamp or datetime.now(UTC)

    reading = SensorReading(
        device_id=device.id,
        timestamp=captured_at,
        temperature=payload.temperature,
        moisture=payload.moisture,
        ambient_temp=payload.ambient_temp,
    )
    device.last_seen = captured_at
    device.is_online = True

    db.add(reading)
    db.add(device)
    db.commit()
    db.refresh(reading)
    return reading
