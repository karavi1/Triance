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

class ExerciseUpdate(ExerciseBase):
    pass

class ExerciseOut(ExerciseBase):
    id: UUID

    model_config = {
        "from_attributes": True  # replaces orm_mode in Pydantic v2
    }

class ExerciseSummaryOut(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }