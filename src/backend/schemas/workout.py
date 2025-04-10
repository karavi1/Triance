from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from src.backend.schemas.logged_exercise import LoggedExerciseCreateByName, LoggedExerciseOut  
from src.backend.models.enums import WorkoutType

class WorkoutBase(BaseModel):
    notes: Optional[str] = None
    workout_type: Optional[WorkoutType] = None

class WorkoutCreate(WorkoutBase):
    user_id: UUID
    logged_exercises: List[LoggedExerciseOut] = Field(..., min_length=1)

class WorkoutCreateSimple(BaseModel):
    username: str
    notes: Optional[str] = None
    logged_exercises: List[LoggedExerciseCreateByName] = Field(..., min_length=1)

class WorkoutUpdate(WorkoutBase):
    notes: Optional[str]

class WorkoutOut(WorkoutBase):
    id: UUID
    user_id: UUID
    created_time: datetime
    logged_exercises: List[LoggedExerciseOut] = []

    model_config = {
        "from_attributes": True
    }