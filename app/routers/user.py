from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.deps import DbSession, get_current_admin, get_current_user
from app.models.user import User, UserRole
from app.schemas.user import UserAdminUpdate, UserProfileRead, UserRead
from app.services.profile import update_user_profile
from app.services.users import get_user_by_email_sync, get_user_by_id, list_users


router = APIRouter(prefix="/user")


@router.patch("/profile", response_model=UserProfileRead)
def patch_user_profile(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
    full_name: Annotated[str | None, Form(min_length=1, max_length=255)] = None,
    email: Annotated[str | None, Form(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", max_length=255)] = None,
    current_password: Annotated[str | None, Form(min_length=8, max_length=128)] = None,
    new_password: Annotated[str | None, Form(min_length=8, max_length=128)] = None,
    avatar: UploadFile | None = File(default=None),
) -> UserProfileRead:
    return update_user_profile(
        db,
        current_user,
        full_name=full_name,
        email=email,
        current_password=current_password,
        new_password=new_password,
        avatar=avatar,
    )


@router.get("/users", response_model=list[UserRead])
def list_all_users(
    db: DbSession,
    _: Annotated[User, Depends(get_current_admin)],
) -> list[UserRead]:
    return list_users(db)


@router.patch("/users/{user_id}", response_model=UserRead)
def patch_user_by_admin(
    user_id: int,
    payload: UserAdminUpdate,
    db: DbSession,
    current_admin: Annotated[User, Depends(get_current_admin)],
) -> UserRead:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if payload.email is not None:
        normalized_email = payload.email.strip().lower()
        existing = get_user_by_email_sync(db, normalized_email)
        if existing and existing.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered.",
            )
        user.email = normalized_email

    if payload.full_name is not None:
        user.full_name = payload.full_name.strip()

    if payload.role is not None:
        user.role = payload.role

    if payload.is_active is not None:
        if user.id == current_admin.id and payload.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot deactivate your own account.",
            )
        user.is_active = payload.is_active

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_admin(
    user_id: int,
    db: DbSession,
    current_admin: Annotated[User, Depends(get_current_admin)],
) -> None:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account.",
        )

    if user.role == UserRole.ADMIN:
        admin_count = db.query(User).filter(User.role == UserRole.ADMIN).count()
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one admin user must remain.",
            )

    db.delete(user)
    db.commit()
