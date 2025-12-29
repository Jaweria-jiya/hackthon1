from pydantic import BaseModel
import uuid
from datetime import datetime

class QuizBase(BaseModel):
    week_number: int
    score: int

class QuizCreate(QuizBase):
    pass

class Quiz(QuizBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True