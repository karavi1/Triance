from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.backend.models.base import Base

class Exercise(Base):
    __tablename__ = 'exercises'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True, nullable=False)
    body_parts: Mapped[list] = mapped_column(JSON, nullable=False)  # ✅ Store as JSON

    def __repr__(self):
        return f'Exercise(id={self.id}, name="{self.name}", body_parts={self.body_parts})'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "body_parts": self.body_parts  # ✅ JSON automatically converts to list
        }