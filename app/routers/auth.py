from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_current_user
from app.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    TokenPair,
    TokenRefreshResponse,
)
from app.schemas.user import UserCreate, UserRead
from app.services.auth import (
    authenticate_user,
    create_user,
    logout_refresh_token,
    refresh_access_token,
)
from app.models.user import User

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db=Depends(get_db)) -> UserRead:
    return await create_user(db, payload)


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, db=Depends(get_db)) -> TokenPair:
    token_pair = await authenticate_user(db, email=payload.email, password=payload.password)
    if not token_pair:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_pair


@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh(payload: RefreshTokenRequest, db=Depends(get_db)) -> TokenRefreshResponse:
    return await refresh_access_token(db, payload.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: LogoutRequest, db=Depends(get_db)) -> None:
    await logout_refresh_token(db, payload.refresh_token)


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: Annotated[User, Depends(get_current_user)]) -> UserRead:
    return current_user
