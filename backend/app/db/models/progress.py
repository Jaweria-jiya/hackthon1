import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    week_number = Column(Integer, nullable=False)
    completion_percent = Column(Integer, nullable=False, default=0)

    user = relationship("User", back_populates="progress")
