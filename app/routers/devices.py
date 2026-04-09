from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.deps import DbSession, get_current_user
from app.models.user import User
from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from app.services.devices import (
    create_device,
    delete_device,
    get_device_for_user,
    list_devices_for_user,
    update_device,
)


router = APIRouter(prefix="/devices")


@router.get("", response_model=list[DeviceRead])
def list_devices(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[DeviceRead]:
    return list_devices_for_user(db, current_user)


@router.post("", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
def add_device(
    payload: DeviceCreate,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> DeviceRead:
    return create_device(db, current_user, payload)


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
