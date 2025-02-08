from backend.schemas.user import User
from backend.schemas.exercise import Exercise
from sqlalchemy.orm import Mapped, mapped_column

class Workout():
    __tablename__ = 'workouts'

    workout_id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[User] = mapped_column(index=True)
    exercise: Mapped[Exercise] = mapped_column(index=True)
    set: Mapped[int] = mapped_column()
    reps: Mapped[int] = mapped_column()
    weight: Mapped[int] = mapped_column()

    def __repr__(self):
        return f'Workout({self.workout_id}, "{self.user}")'
