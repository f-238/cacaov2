from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.deps import DbSession, get_current_user
from app.models.user import User
from app.schemas.device import (
    DeviceCreate,
    DeviceIngestTokenRead,
    DeviceProvisionRead,
    DeviceRead,
    DeviceUpdate,
)
from app.services.devices import (
    create_device,
    delete_device,
    get_device_for_user,
    list_devices_for_user,
    rotate_device_ingest_token,
    update_device,
)


router = APIRouter(prefix="/devices")


@router.get("", response_model=list[DeviceRead])
def list_devices(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[DeviceRead]:
    return list_devices_for_user(db, current_user)


@router.post("", response_model=DeviceProvisionRead, status_code=status.HTTP_201_CREATED)
def add_device(
    payload: DeviceCreate,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> DeviceProvisionRead:
    device, ingest_token = create_device(db, current_user, payload)
    return DeviceProvisionRead.model_validate(
        {
            "id": device.id,
            "device_name": device.device_name,
            "device_serial": device.device_serial,
            "user_id": device.user_id,
            "last_seen": device.last_seen,
            "is_online": device.is_online,
            "firmware_version": device.firmware_version,
            "created_at": device.created_at,
            "updated_at": device.updated_at,
            "ingest_token": ingest_token,
        }
    )


@router.post("/{id}/ingest-token", response_model=DeviceIngestTokenRead)
def rotate_ingest_token(
    id: int,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> DeviceIngestTokenRead:
    device, ingest_token = rotate_device_ingest_token(db, current_user, id)
    return DeviceIngestTokenRead(
        device_id=device.id,
        device_serial=device.device_serial,
        ingest_token=ingest_token,
        issued_at=device.ingest_token_created_at,
    )


@router.get("/{id}", response_model=DeviceRead)
def get_device(
    id: int,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> DeviceRead:
    return get_device_for_user(db, current_user, id)


@router.put("/{id}", response_model=DeviceRead)
def update_device_info(
    id: int,
    payload: DeviceUpdate,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> DeviceRead:
    return update_device(db, current_user, id, payload)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def remove_device(
    id: int,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    delete_device(db, current_user, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
