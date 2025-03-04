from pydantic import BaseModel
from typing import List, Optional

class ExerciseBase(BaseModel):
    name: str
    body_parts: List[str]  # Now a list of strings

class ExerciseCreate(ExerciseBase):
    pass  # Used for input validation when creating an exercise

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    body_parts: Optional[List[str]] = None  # Optional list for partial updates

class ExerciseResponse(ExerciseBase):
    id: int

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models