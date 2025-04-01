# src/backend/schemas/exercise.py
from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List

class ExerciseBase(BaseModel):
    name: str
    body_parts: List[str]
    description: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseUpdate(ExerciseBase):
    pass

class ExerciseOut(ExerciseBase):
    id: UUID

    model_config = {
        "from_attributes": True  # replaces orm_mode in Pydantic v2
    }
