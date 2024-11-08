from pydantic import BaseModel
from backend.schemas.user import User
from backend.schemas.exercise import Exercise

class Workout(BaseModel):
    workout_id: int
    user: User
    exercise: list[Exercise]

print("workout.py ran successfully")