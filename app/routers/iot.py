from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status

from app.deps import DbSession
from app.schemas.iot import IoTReadingIngestRequest, IoTReadingIngestResponse
from app.services.iot import ingest_sensor_reading


router = APIRouter(prefix="/iot")


@router.post("/readings", response_model=IoTReadingIngestResponse)
def ingest_reading(
    payload: IoTReadingIngestRequest,
    db: DbSession,
    x_device_token: Annotated[str | None, Header(alias="X-Device-Token")] = None,
) -> IoTReadingIngestResponse:
    if not x_device_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Device-Token header.",
        )

    reading = ingest_sensor_reading(db, x_device_token, payload)
    return IoTReadingIngestResponse(
        reading_id=reading.id,
        device_id=reading.device_id,
        device_serial=payload.device_serial,
        timestamp=reading.timestamp,
    )
