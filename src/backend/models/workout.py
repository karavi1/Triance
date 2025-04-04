from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from datetime import date
from typing import Optional, List
from src.backend.models.base import Base
from src.backend.models.logged_exercise import LoggedExercise

class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    workout_date: Mapped[date] = mapped_column(default=date.today)
    notes: Mapped[Optional[str]] = mapped_column(String(5000), default=None)
    logged_exercises: Mapped[List[LoggedExercise]] = relationship("LoggedExercise", cascade="all, delete-orphan")

    def __repr__(self):
        return f'Workout(id={self.id}, user_id={self.user_id}, workout_date={self.workout_date}, logged_exercises={self.logged_exercises})'

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "workout_date": self.workout_date,
            "logged_exercises": [le.to_dict() for le in self.logged_exercises]
        }