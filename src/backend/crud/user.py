from sqlalchemy.orm import Session
from src.backend.models.user import User

def create_user(db: Session, name: str, email: str):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, name: str = None, email: str = None):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    if name:
        user.name = name
    if email:
        user.email = email
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return True