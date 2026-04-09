from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.alert import AlertSeverity


class AlertRead(BaseModel):
    id: int
    device_id: int
    user_id: int
    type: str
    severity: AlertSeverity
    message: str
    resolved: bool
    created_at: datetime
    resolved_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class AlertResolveRequest(BaseModel):
    alert_id: int
