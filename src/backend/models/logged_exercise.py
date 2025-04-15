from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from typing import List
from src.backend.models.base import Base
from src.backend.models.exercise import Exercise
from src.backend.models.logged_exercise_set import LoggedExerciseSet

class LoggedExercise(Base):
    __tablename__ = 'logged_exercises'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    workout_id: Mapped[UUID] = mapped_column(ForeignKey("workouts.id"))
    exercise_id: Mapped[UUID] = mapped_column(ForeignKey("exercises.id"))

    sets: Mapped[List[LoggedExerciseSet]] = relationship(
        LoggedExerciseSet,
        back_populates="logged_exercise",
        cascade="all, delete-orphan"
    )

    exercise: Mapped[Exercise] = relationship(Exercise, lazy="joined")

    def __repr__(self):
        return f"<LoggedExercise(workout_id={self.workout_id}, exercise_id={self.exercise_id})>"
