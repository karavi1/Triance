from pydantic import BaseModel
from typing import List, Optional

class ExerciseBase(BaseModel):
    name: str
    body_parts: List[str]  # A list of body parts as strings
    description: Optional[str] = None  # Optional description field

class ExerciseCreate(ExerciseBase):
    pass  # Used for input validation when creating an exercise

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    body_parts: Optional[List[str]] = None  # Optional list for partial updates
    description: Optional[str] = None  # Optional update for description

class ExerciseResponse(ExerciseBase):
    id: int

    class Config:
        orm_mode = True  # Allows conversion from SQLAlchemy models
