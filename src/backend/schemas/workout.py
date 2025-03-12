from pydantic import BaseModel
from typing import List, Optional
from .logged_exercise import LoggedExerciseCreate

class WorkoutBase(BaseModel):
    user_id: int
    date: Optional[str] = None
    exercises: List[LoggedExerciseCreate]

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutResponse(WorkoutBase):
    id: int

    class Config:
        orm_mode = True