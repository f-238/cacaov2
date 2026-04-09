from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User, UserRole
from app.utils.jwt import decode_token


DbSession = Annotated[AsyncSession, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    db: DbSession,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        subject = payload.get("sub")
        token_type = payload.get("type")
    except JWTError as exc:
        raise credentials_exception from exc

    if not subject or token_type != "access":
        raise credentials_exception

    result = await db.execute(select(User).where(User.email == subject))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise credentials_exception

    return user


async def get_current_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges are required.",
        )

    return current_user
