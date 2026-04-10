from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.security import get_password_hash, verify_password


AVATAR_UPLOAD_DIR = Path("uploads") / "avatars"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_AVATAR_SIZE_BYTES = 5 * 1024 * 1024


def update_user_profile(
    db: Session,
    user: User,
    *,
    full_name: str | None,
    email: str | None,
    current_password: str | None,
    new_password: str | None,
    avatar: UploadFile | None,
) -> User:
    if full_name is not None:
        user.full_name = full_name.strip()

    if email is not None:
        normalized_email = email.strip().lower()
        if normalized_email != user.email:
            existing_user = (
                db.query(User)
                .filter(User.email == normalized_email, User.id != user.id)
                .first()
            )
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email is already registered.",
                )
            user.email = normalized_email

    if new_password is not None:
        if not current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is required to set a new password.",
            )
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect.",
            )
        user.hashed_password = get_password_hash(new_password)

    if avatar is not None:
        user.avatar_url = _save_avatar(avatar, user.avatar_url)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _save_avatar(file: UploadFile, previous_avatar_url: str | None) -> str:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar file must have a filename.",
        )

    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported avatar file type.",
        )

    content_type = (file.content_type or "").lower()
    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar must be an image file.",
        )

    file_bytes = file.file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar file is empty.",
        )
    if len(file_bytes) > MAX_AVATAR_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar file exceeds 5MB limit.",
        )

    AVATAR_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{extension}"
    destination = AVATAR_UPLOAD_DIR / filename
    destination.write_bytes(file_bytes)

    _delete_previous_avatar(previous_avatar_url)
    return f"/uploads/avatars/{filename}"


def _delete_previous_avatar(previous_avatar_url: str | None) -> None:
    if not previous_avatar_url or not previous_avatar_url.startswith("/uploads/avatars/"):
        return

    previous_file = Path(previous_avatar_url.lstrip("/"))
    if previous_file.exists() and previous_file.is_file():
        previous_file.unlink()
