from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional, List
from src.backend.models.base import Base
from src.backend.models.logged_exercise import LoggedExercise

class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    created_time: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    notes: Mapped[Optional[str]] = mapped_column(String(5000), default=None)
    logged_exercises: Mapped[List[LoggedExercise]] = relationship("LoggedExercise", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'Workout(id={self.id}, user_id={self.user_id}, created_time={self.created_time}, logged_exercises={self.logged_exercises})'

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_time": self.created_time,  # updated field name
            "logged_exercises": [le.to_dict() for le in self.logged_exercises]
        }
