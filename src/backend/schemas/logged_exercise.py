from pydantic import BaseModel, Field
from src.backend.schemas.exercise import ExerciseSummaryOut
from uuid import UUID

class LoggedExerciseBase(BaseModel):
    exercise_id: UUID
    sets: int = Field(..., ge=0)
    reps: int = Field(..., ge=0)
    weight: float = Field(..., ge=0)

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
    sets: int = Field(..., ge=0)
    reps: int = Field(..., ge=0)
    weight: float = Field(..., ge=0)