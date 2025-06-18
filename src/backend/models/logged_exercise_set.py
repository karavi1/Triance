from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import UUID, uuid4
from src.backend.models.base import Base

class LoggedExerciseSet(Base):
    __tablename__ = "logged_exercise_sets"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    logged_exercise_id: Mapped[UUID] = mapped_column(ForeignKey("logged_exercises.id"))
    set_number: Mapped[int]
    reps: Mapped[int]
    weight: Mapped[float]

    logged_exercise = relationship("LoggedExercise", back_populates="sets")

    def __repr__(self):
        return f"<Set {self.set_number}: {self.reps} reps @ {self.weight} lbs>"