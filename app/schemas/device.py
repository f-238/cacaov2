from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DeviceBase(BaseModel):
    device_name: str = Field(min_length=1, max_length=255)
    device_serial: str = Field(min_length=1, max_length=255)
    last_seen: datetime | None = None
    is_online: bool = False
    firmware_version: str | None = Field(default=None, max_length=100)


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    device_name: str | None = Field(default=None, min_length=1, max_length=255)
    device_serial: str | None = Field(default=None, min_length=1, max_length=255)
    last_seen: datetime | None = None
    is_online: bool | None = None
    firmware_version: str | None = Field(default=None, max_length=100)


class DeviceRead(DeviceBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceProvisionRead(DeviceRead):
    ingest_token: str


class DeviceIngestTokenRead(BaseModel):
    device_id: int
    device_serial: str
    ingest_token: str
    issued_at: datetime
