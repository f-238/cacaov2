from datetime import UTC, datetime

from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import TokenPair, TokenRefreshResponse
from app.schemas.user import UserCreate
from app.services.users import get_user_by_email
from app.utils.jwt import create_access_token, create_refresh_token, decode_token
from app.utils.security import get_password_hash, verify_password


async def ensure_default_admin_user(db: AsyncSession) -> None:
    result = await db.execute(select(User).where(User.email == "admin@cacaomonitor.local"))
    existing_admin = result.scalar_one_or_none()
    if existing_admin:
        return

    admin_user = User(
        full_name="System Administrator",
        email="admin@cacaomonitor.local",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        is_active=True,
    )
    db.add(admin_user)
    await db.commit()


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    existing_user = await get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    user = User(
        full_name=payload.full_name,
        email=payload.email.lower(),
        hashed_password=get_password_hash(payload.password),
        role=payload.role,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> TokenPair | None:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None

    access_token = create_access_token(user.email, user.role)
    refresh_token, expires_at = create_refresh_token(user.email, user.role)

    refresh_record = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at,
        revoked=False,
    )
    db.add(refresh_record)
    await db.commit()

    return TokenPair(access_token=access_token, refresh_token=refresh_token)


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> TokenRefreshResponse:
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == refresh_token))
    refresh_record = result.scalar_one_or_none()

    if not refresh_record or refresh_record.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is invalid or revoked.",
        )

    if refresh_record.expires_at < datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired.",
        )

    try:
        payload = decode_token(refresh_token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token could not be verified.",
        ) from exc

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token type is invalid for refresh.",
        )

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token subject is missing.",
        )

    user = await get_user_by_email(db, subject)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists.",
        )

    access_token = create_access_token(subject, user.role)
    return TokenRefreshResponse(access_token=access_token)


async def logout_refresh_token(db: AsyncSession, refresh_token: str) -> None:
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == refresh_token))
    refresh_record = result.scalar_one_or_none()

    if not refresh_record:
        return

    refresh_record.revoked = True
    db.add(refresh_record)
    await db.commit()
