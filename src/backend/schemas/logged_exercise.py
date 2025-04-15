from pydantic import BaseModel
from uuid import UUID
from typing import List
from src.backend.schemas.exercise import ExerciseSummaryOut
from src.backend.schemas.logged_exercise_set import LoggedExerciseSetCreate, LoggedExerciseSetOut

class LoggedExerciseBase(BaseModel):
    exercise_id: UUID

class LoggedExerciseCreate(LoggedExerciseBase):
    sets: List[LoggedExerciseSetCreate]

class LoggedExerciseUpdate(LoggedExerciseBase):
    sets: List[LoggedExerciseSetCreate]

class LoggedExerciseOut(BaseModel):
    id: UUID
    workout_id: UUID
    exercise: ExerciseSummaryOut
    sets: List[LoggedExerciseSetOut]

    model_config = {
        "from_attributes": True
    }

class LoggedExerciseCreateByName(BaseModel):
    name: str
    sets: List[LoggedExerciseSetCreate]