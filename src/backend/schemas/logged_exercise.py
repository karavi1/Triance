# src/backend/schemas/logged_exercise.py
from pydantic import BaseModel
from src.backend.schemas.exercise import ExerciseSummaryOut
from uuid import UUID

class LoggedExerciseBase(BaseModel):
    exercise_id: UUID
    sets: int
    reps: int
    weight: float

class LoggedExerciseCreate(LoggedExerciseBase):
    pass

class LoggedExerciseUpdate(LoggedExerciseBase):
    pass

class LoggedExerciseOut(BaseModel):
    id: UUID
    workout_id: UUID
    sets: int
    reps: int
    weight: float
    exercise: ExerciseSummaryOut

    model_config = {
        "from_attributes": True
    }

class LoggedExerciseCreateByName(BaseModel):
    name: str
    sets: int
    reps: int
    weight: float