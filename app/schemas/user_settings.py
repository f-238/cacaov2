from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


HEX_COLOR_PATTERN = r"^#[0-9A-Fa-f]{6}$"


class UserSettingsRead(BaseModel):
    id: int
    user_id: int
    theme_mode: str
    font_size: str
    primary_color: str
    secondary_color: str
    accent_color: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserSettingsUpdate(BaseModel):
    theme_mode: Literal["light", "dark", "system"]
    font_size: Literal["small", "medium", "large"]
    primary_color: str = Field(pattern=HEX_COLOR_PATTERN)
    secondary_color: str = Field(pattern=HEX_COLOR_PATTERN)
    accent_color: str = Field(pattern=HEX_COLOR_PATTERN)
