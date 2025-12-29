from pydantic import BaseModel
import uuid
from datetime import datetime

class NoteBase(BaseModel):
    content: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True