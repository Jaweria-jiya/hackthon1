from pydantic import BaseModel
from datetime import datetime
import uuid

class UserActivityLogBase(BaseModel):
    action: str
    resource_id: str | None = None

class UserActivityLogCreate(UserActivityLogBase):
    user_id: uuid.UUID
    email: str

class UserActivityLog(UserActivityLogBase):
    id: int
    user_id: uuid.UUID
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
