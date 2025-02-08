from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class User():
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)

    def __repr__(self):
        return f'User({self.user_id}, "{self.name}")'