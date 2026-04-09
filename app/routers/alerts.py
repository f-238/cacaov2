from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.deps import DbSession, get_current_user
from app.models.user import User
from app.schemas.alert import AlertRead, AlertResolveRequest
from app.services.alerts import list_alerts_for_device, resolve_alert_for_device


router = APIRouter(prefix="/devices/{id}/alerts")


@router.get("", response_model=list[AlertRead])
def list_device_alerts(
    id: int,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
    resolved: bool | None = Query(default=None),
) -> list[AlertRead]:
    return list_alerts_for_device(db, current_user, id, resolved)


@router.post("/resolve", response_model=AlertRead)
def resolve_device_alert(
    id: int,
    payload: AlertResolveRequest,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> AlertRead:
    return resolve_alert_for_device(db, current_user, id, payload.alert_id)
