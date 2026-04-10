from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.user import UserRole

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class UserBase(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: str = Field(pattern=EMAIL_PATTERN, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.USER


class UserRead(UserBase):
    id: int
    role: UserRole
    is_active: bool
    avatar_url: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserProfileRead(BaseModel):
    id: int
    full_name: str
    email: str = Field(pattern=EMAIL_PATTERN, max_length=255)
    avatar_url: str | None = None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserAdminUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = Field(default=None, pattern=EMAIL_PATTERN, max_length=255)
    role: UserRole | None = None
    is_active: bool | None = None
