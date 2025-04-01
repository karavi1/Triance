# src/backend/schemas/workout.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from src.backend.schemas.logged_exercise import LoggedExerciseOut  # import depends on your structure

class WorkoutBase(BaseModel):
    date: Optional[datetime] = None
    notes: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    user_id: UUID
    exercises: List[LoggedExerciseOut]  # during creation, if you're sending logs too

class WorkoutUpdate(WorkoutBase):
    notes: Optional[str]

class WorkoutOut(WorkoutBase):
    id: UUID
    user_id: UUID
    date: datetime
    exercises: List[LoggedExerciseOut] = []

    model_config = {
        "from_attributes": True
    }
