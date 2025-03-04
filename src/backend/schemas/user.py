from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass  # Used for creating a new user

class UserResponse(UserBase):
    user_id: int  # Ensure this matches your DB model field

    class Config:
        from_attributes = True  # Enables ORM mode