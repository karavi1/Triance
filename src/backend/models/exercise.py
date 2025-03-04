from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from typing import List
from src.backend.models.base import Base

class Exercise(Base):
    __tablename__ = 'exercises'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True, nullable=False)
    body_parts: Mapped[str] = mapped_column(String(256), nullable=False)  # Store as comma-separated string

    def __repr__(self):
        return f'Exercise(id={self.id}, name="{self.name}", body_parts="{self.body_parts}")'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "body_parts": self.body_parts.split(",")  # Convert stored string to list
        }