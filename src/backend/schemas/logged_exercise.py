# src/backend/schemas/logged_exercise.py
from pydantic import BaseModel
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

class LoggedExerciseOut(LoggedExerciseBase):
    id: UUID
    workout_id: UUID

    model_config = {
        "from_attributes": True
    }
