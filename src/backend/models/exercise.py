from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from typing import Optional, List
from src.backend.models.base import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255))
    body_parts: Mapped[list[str]] = mapped_column(JSON)
    description: Mapped[Optional[str]] = mapped_column(String(500), default=None)

    def __repr__(self):
        return f'Exercise(id={self.id}, name="{self.name}", body_parts={self.body_parts})'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "body_parts": self.body_parts,
            "description": self.description  # Include description in the dict output
        }