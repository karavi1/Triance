from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from src.backend.models.auth_user import AuthUser
from src.backend.schemas.auth_user import AuthUserCreate, AuthUserUpdate
from src.backend.auth.util import get_password_hash

def get_user_by_id(db: Session, user_id: UUID) -> Optional[AuthUser]:
    return db.query(AuthUser).filter(AuthUser.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[AuthUser]:
    return db.query(AuthUser).filter(AuthUser.username == username).first()

def get_all_users(db: Session) -> List[AuthUser]:
    return db.query(AuthUser).all()

def create_user(db: Session, user_data: AuthUserCreate) -> AuthUser:
    hashed_password = get_password_hash(user_data.password)
    db_user = AuthUser(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        disabled=user_data.disabled or False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: UUID, updates: AuthUserUpdate) -> Optional[AuthUser]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    update_data = updates.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: UUID) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True