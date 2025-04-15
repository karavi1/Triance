from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class LoggedExerciseSetBase(BaseModel):
    set_number: int = Field(..., ge=1)
    reps: int = Field(..., ge=0)
    weight: float = Field(..., ge=0)

class LoggedExerciseSetCreate(LoggedExerciseSetBase):
    pass

class LoggedExerciseSetOut(LoggedExerciseSetBase):
    id: UUID
    logged_exercise_id: UUID

    model_config = {
        "from_attributes": True
    }
