from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt

from app.config import get_settings
from app.models.user import UserRole


settings = get_settings()


def create_token(
    subject: str,
    role: UserRole,
    token_type: str,
    expires_delta: timedelta,
) -> tuple[str, datetime]:
    expires_at = datetime.now(UTC) + expires_delta
    payload = {
        "sub": subject,
        "role": role.value,
        "type": token_type,
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token, expires_at


def create_access_token(subject: str, role: UserRole) -> str:
    token, _ = create_token(
        subject=subject,
        role=role,
        token_type="access",
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return token


def create_refresh_token(subject: str, role: UserRole) -> tuple[str, datetime]:
    return create_token(
        subject=subject,
        role=role,
        token_type="refresh",
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
