from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class AuthUserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class AuthUserCreate(AuthUserBase):
    password: str

class AuthUserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    password: Optional[str] = None

class AuthUserOut(AuthUserBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None