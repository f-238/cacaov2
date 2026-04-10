from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_sync_db
from app.models.user import User, UserRole
from app.utils.jwt import decode_token


DbSession = Annotated[Session, Depends(get_sync_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
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

    user = db.query(User).filter(User.email == subject).first()
    if not user or not user.is_active:
        raise credentials_exception

    return user


def get_current_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges are required.",
        )

    return current_user
