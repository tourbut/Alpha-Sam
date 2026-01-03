from typing import Optional
from pydantic import BaseModel, ConfigDict

class NotificationSettingsBase(BaseModel):
    daily_report_enabled: bool = True
    price_alert_enabled: bool = True

class NotificationSettingsUpdate(NotificationSettingsBase):
    pass

class NotificationSettingsRead(NotificationSettingsBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)
