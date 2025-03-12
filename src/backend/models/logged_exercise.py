from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.backend.models.base import Base

class LoggedExercise(Base):
    __tablename__ = 'logged_exercises'

    workout_id: Mapped[int] = mapped_column(Integer, ForeignKey('workouts.id'), primary_key=True)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey('exercises.id'), primary_key=True)
    weight: Mapped[float] = mapped_column(Float)
    sets: Mapped[int] = mapped_column(Integer)
    reps: Mapped[int] = mapped_column(Integer)

    workout: Mapped["Workout"] = relationship("Workout", back_populates="exercises")  # ✅ Use string reference
    exercise: Mapped["Exercise"] = relationship("Exercise")  # ✅ Use string reference

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
