from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorReadingRead(BaseModel):
    id: int
    device_id: int
    timestamp: datetime
    temperature: float
    moisture: float
    ambient_temp: float

    model_config = ConfigDict(from_attributes=True)


class SensorReadingSummary(BaseModel):
    count: int
    avg_temperature: float | None
    min_temperature: float | None
    max_temperature: float | None
    avg_moisture: float | None
    min_moisture: float | None
    max_moisture: float | None
    avg_ambient_temp: float | None
    min_ambient_temp: float | None
    max_ambient_temp: float | None


class SensorReadingExportRequest(BaseModel):
    format: str = Field(default="csv", pattern="^(csv|excel)$")
