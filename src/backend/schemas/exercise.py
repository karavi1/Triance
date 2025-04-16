from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from src.backend.models.enums import ExerciseGroup

class ExerciseBase(BaseModel):
    name: str
    category: ExerciseGroup
    primary_muscles: List[str]
    secondary_muscles: Optional[List[str]] = None
    description: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[ExerciseGroup] = None
    primary_muscles: Optional[List[str]] = None
    secondary_muscles: Optional[List[str]] = None
    description: Optional[str] = None

class ExerciseOut(BaseModel):
    id: UUID
    name: str
    category: ExerciseGroup
    primary_muscles: List[str]
    secondary_muscles: Optional[List[str]] = None
    description: Optional[str] = None

    model_config = {
        "from_attributes": True  # Required to serialize SQLAlchemy models
    }

class ExerciseSummaryOut(BaseModel):
    id: UUID
    name: str
    category: ExerciseGroup

    model_config = {
        "from_attributes": True
    }