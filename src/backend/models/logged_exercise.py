from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from src.backend.models.base import Base

class LoggedExercise(Base):
    __tablename__ = 'logged_exercises'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    workout_id: Mapped[UUID] = mapped_column(ForeignKey("workouts.id"))
    exercise_id: Mapped[UUID] = mapped_column(ForeignKey("exercises.id"))
    sets: Mapped[int]
    reps: Mapped[int]
    weight: Mapped[float]

    def __repr__(self):
        return f'LoggedExercise(workout_id={self.workout_id}, exercise_id={self.exercise_id}, weight={self.weight}, sets={self.sets}, reps={self.reps})'

    def to_dict(self):
        return {
            "workout_id": self.workout_id,
            "exercise_id": self.exercise_id,
            "weight": self.weight,
            "sets": self.sets,
            "reps": self.reps
        }
