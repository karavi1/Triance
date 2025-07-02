from sqlalchemy import JSON, String, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from typing import Optional, List
from src.backend.models.auth_user import AuthUser
from src.backend.models.base import Base
from src.backend.models.enums import ExerciseGroup

class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth_users.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    category: Mapped[ExerciseGroup] = mapped_column(SQLEnum(ExerciseGroup), nullable=True)
    primary_muscles: Mapped[list[str]] = mapped_column(JSON)
    secondary_muscles: Mapped[Optional[list[str]]] = mapped_column(JSON)
    description: Mapped[Optional[str]] = mapped_column(String(5000), default=None)

    user: Mapped[AuthUser] = relationship("AuthUser", backref="exercises")

    def __repr__(self):
        return f'Exercise(id={self.id}, name="{self.name}", primary_body_parts={self.primary_body_parts}, secondary_muscles={self.secondary_muscles})'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "primary_muscles": self.primary_muscles,
            "secondary_muscles": self.secondary_muscles,
            "description": self.description
        }