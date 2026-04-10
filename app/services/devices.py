from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.user import User
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.utils.device_tokens import generate_device_token, hash_device_token


def list_devices_for_user(db: Session, user: User) -> list[Device]:
    return (
        db.query(Device)
        .filter(Device.user_id == user.id)
        .order_by(Device.id.asc())
        .all()
    )


def get_device_for_user(db: Session, user: User, device_id: int) -> Device:
    device = (
        db.query(Device)
        .filter(Device.id == device_id, Device.user_id == user.id)
        .first()
    )

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found.",
        )

    return device


def create_device(db: Session, user: User, payload: DeviceCreate) -> tuple[Device, str]:
    existing_device = (
        db.query(Device)
        .filter(Device.device_serial == payload.device_serial)
        .first()
    )
    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device serial is already registered.",
        )

    ingest_token = generate_device_token()
    device = Device(
        device_name=payload.device_name,
        device_serial=payload.device_serial,
        user_id=user.id,
        last_seen=payload.last_seen,
        is_online=payload.is_online,
        firmware_version=payload.firmware_version,
        ingest_token_hash=hash_device_token(ingest_token),
        ingest_token_created_at=datetime.now(UTC),
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device, ingest_token


def update_device(db: Session, user: User, device_id: int, payload: DeviceUpdate) -> Device:
    device = get_device_for_user(db, user, device_id)

    if payload.device_serial and payload.device_serial != device.device_serial:
        existing_device = (
            db.query(Device)
            .filter(Device.device_serial == payload.device_serial, Device.id != device.id)
            .first()
        )
        if existing_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device serial is already registered.",
            )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device, field, value)

    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def rotate_device_ingest_token(db: Session, user: User, device_id: int) -> tuple[Device, str]:
    device = get_device_for_user(db, user, device_id)
    ingest_token = generate_device_token()
    device.ingest_token_hash = hash_device_token(ingest_token)
    device.ingest_token_created_at = datetime.now(UTC)

    db.add(device)
    db.commit()
    db.refresh(device)
    return device, ingest_token


def delete_device(db: Session, user: User, device_id: int) -> None:
    device = get_device_for_user(db, user, device_id)
    db.delete(device)
    db.commit()
