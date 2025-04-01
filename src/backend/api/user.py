from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.backend.database.configure import get_db
from src.backend.schemas.user import UserCreate
from src.backend.crud.user import create_user, get_user_by_id, delete_user, get_all_users

router = APIRouter()

@router.post("/")
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/{user_id}")
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
def get_every_user(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.delete("/{user_id}")
def delete_this_user(user_id: UUID, db: Session = Depends(get_db)):
    return delete_user(db, user_id)