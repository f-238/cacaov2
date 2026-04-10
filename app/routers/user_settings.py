from typing import Annotated

from fastapi import APIRouter, Depends

from app.deps import DbSession, get_current_user
from app.models.user import User
from app.schemas.user_settings import UserSettingsRead, UserSettingsUpdate
from app.services.user_settings import (
    get_or_create_settings_for_user,
    update_settings_for_user,
)


router = APIRouter(prefix="/user")


@router.get("/settings", response_model=UserSettingsRead)
def get_current_user_settings(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserSettingsRead:
    return get_or_create_settings_for_user(db, current_user)


@router.put("/settings", response_model=UserSettingsRead)
def update_current_user_settings(
    payload: UserSettingsUpdate,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserSettingsRead:
    return update_settings_for_user(db, current_user, payload)
