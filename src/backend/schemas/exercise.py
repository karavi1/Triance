from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class Exercise():
    __tablename__ = 'exercises'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    body_parts: Mapped[str] = mapped_column(String(64), unique=True)

    def __repr__(self):
        return f'Exercise({self.id}, "{self.name}")'