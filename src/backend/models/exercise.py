from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.backend.models.base import Base
from src.backend.models.logged_exercise import LoggedExercise  # Import the LoggedExercise model
from typing import Optional

class Exercise(Base):
    __tablename__ = 'exercises'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True, nullable=False)
    body_parts: Mapped[list] = mapped_column(JSON, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)  # Optional description field

    exercises_logged: Mapped[list[LoggedExercise]] = relationship("LoggedExercise", back_populates="exercise")

    def __repr__(self):
        return f'Exercise(id={self.id}, name="{self.name}", body_parts={self.body_parts})'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "body_parts": self.body_parts,
            "description": self.description  # Include description in the dict output
        }