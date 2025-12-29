from pydantic import BaseModel
import uuid

class ProgressBase(BaseModel):
    week_number: int
    completion_percent: int

class ProgressCreate(ProgressBase):
    pass

class Progress(ProgressBase):
    id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        from_attributes = True