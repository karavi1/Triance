from sqlalchemy import Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.backend.models.base import Base
from src.backend.models.logged_exercise import LoggedExercise  # Import LoggedExercise model

class Workout(Base):
    __tablename__ = 'workouts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    date: Mapped[Date] = mapped_column(Date, default=datetime.utcnow)

    exercises: Mapped[list[LoggedExercise]] = relationship("LoggedExercise", back_populates="workout")

    def __repr__(self):
        return f'Workout(id={self.id}, user_id={self.user_id}, date={self.date})'

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date,
            "exercises": [exercise.to_dict() for exercise in self.exercises]
        }
