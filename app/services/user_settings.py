from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_settings import UserSettings
from app.schemas.user_settings import UserSettingsUpdate


def get_or_create_settings_for_user(db: Session, user: User) -> UserSettings:
    settings = db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
    if settings:
        return settings

    settings = UserSettings(user_id=user.id)
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


def update_settings_for_user(
    db: Session,
    user: User,
    payload: UserSettingsUpdate,
) -> UserSettings:
    settings = get_or_create_settings_for_user(db, user)
    settings.theme_mode = payload.theme_mode
    settings.font_size = payload.font_size
    settings.primary_color = payload.primary_color
    settings.secondary_color = payload.secondary_color
    settings.accent_color = payload.accent_color

    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings
