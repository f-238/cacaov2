from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.deps import DbSession, get_current_user
from app.models.user import User
from app.schemas.sensor_reading import (
    SensorReadingExportRequest,
    SensorReadingRead,
    SensorReadingSummary,
)
from app.services.sensor_readings import (
    export_readings_for_device,
    get_latest_reading_for_device,
    get_readings_summary_for_device,
    list_readings_for_device,
)


router = APIRouter(prefix="/devices/{id}/readings")


@router.get("", response_model=list[SensorReadingRead])
def list_device_readings(
    id: int,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[SensorReadingRead]:
    return list_readings_for_device(db, current_user, id)


@router.get("/latest", response_model=SensorReadingRead)
def latest_device_reading(
    id: int,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> SensorReadingRead:
    return get_latest_reading_for_device(db, current_user, id)


@router.get("/summary", response_model=SensorReadingSummary)
def device_readings_summary(
    id: int,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> SensorReadingSummary:
    return get_readings_summary_for_device(db, current_user, id)


@router.post("/export")
def export_device_readings(
    id: int,
    payload: SensorReadingExportRequest,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> StreamingResponse:
    file_bytes, media_type, filename = export_readings_for_device(
        db,
        current_user,
        id,
        payload.format,
    )

    return StreamingResponse(
        iter([file_bytes]),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
