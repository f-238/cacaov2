from datetime import UTC, datetime

from pydantic import BaseModel, Field


class IoTReadingIngestRequest(BaseModel):
    device_serial: str = Field(min_length=1, max_length=255)
    temperature: float
    moisture: float
    ambient_temp: float
    timestamp: datetime | None = None


class IoTReadingIngestResponse(BaseModel):
    reading_id: int
    device_id: int
    device_serial: str
    timestamp: datetime
    accepted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
