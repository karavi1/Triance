from sqlalchemy import Column, Integer, String
from src.backend.models.base import Base

# User Model
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), index=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)

    def __repr__(self):
        return f'User({self.user_id}, "{self.name}", "{self.email}")'