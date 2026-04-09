from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.alert import DeviceAlert
from app.models.user import User
from app.services.devices import get_device_for_user


def list_alerts_for_device(
    db: Session,
    user: User,
    device_id: int,
    resolved: bool | None,
) -> list[DeviceAlert]:
    device = get_device_for_user(db, user, device_id)

    query = db.query(DeviceAlert).filter(DeviceAlert.device_id == device.id)
    if resolved is not None:
        query = query.filter(DeviceAlert.resolved == resolved)

    return query.order_by(DeviceAlert.created_at.desc()).all()


def resolve_alert_for_device(
    db: Session,
    user: User,
    device_id: int,
    alert_id: int,
) -> DeviceAlert:
    device = get_device_for_user(db, user, device_id)
    alert = (
        db.query(DeviceAlert)
        .filter(
            DeviceAlert.id == alert_id,
            DeviceAlert.device_id == device.id,
            DeviceAlert.user_id == user.id,
        )
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    if not alert.resolved:
        alert.resolved = True
        alert.resolved_at = datetime.now(UTC)
        db.add(alert)
        db.commit()
        db.refresh(alert)

    return alert
