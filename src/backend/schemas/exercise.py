from pydantic import BaseModel
from typing import Tuple

class Exercise(BaseModel):
    exercise_id: int
    name: str
    body_part: str
    unit: list[Tuple[int, int]] # [(weight, rep), (weight, rep), ...]

print("exercise.py ran successfully")