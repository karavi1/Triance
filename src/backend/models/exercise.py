from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from typing import Optional, List
from src.backend.models.base import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    primary_muscles: Mapped[list[str]] = mapped_column(JSON)
    secondary_muscles: Mapped[Optional[list[str]]] = mapped_column(JSON)
    description: Mapped[Optional[str]] = mapped_column(String(5000), default=None)

    def __repr__(self):
        return f'Exercise(id={self.id}, name="{self.name}", primary_body_parts={self.primary_body_parts}, secondary_muscles={self.secondary_muscles})'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "primary_muscles": self.primary_muscles,
            "secondary_muscles": self.secondary_muscles,
            "description": self.description  # Include description in the dict output
        }