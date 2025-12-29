import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    week_number = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
