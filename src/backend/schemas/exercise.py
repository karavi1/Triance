from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List

class ExerciseBase(BaseModel):
    name: str
    primary_muscles: List[str]
    secondary_muscles: Optional[List[str]] = None
    description: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    primary_muscles: Optional[List[str]] = None
    secondary_muscles: Optional[List[str]] = None
    description: Optional[str] = None

class ExerciseOut(BaseModel):
    id: UUID
    name: str
    primary_muscles: List[str]
    secondary_muscles: Optional[List[str]] = None
    description: Optional[str] = None

    model_config = {
        "from_attributes": True  # Required to serialize SQLAlchemy models
    }

class ExerciseSummaryOut(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }