from pydantic import BaseModel
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from typing import Optional
from src.backend.models.base import Base

class AuthUser(Base):
    __tablename__ = "auth_users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    disabled: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f'AuthUser(id={self.id}, username="{self.username}", email="{self.email}", disabled={self.disabled})'

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "disabled": self.disabled,
            "is_admin": self.is_admin
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None
