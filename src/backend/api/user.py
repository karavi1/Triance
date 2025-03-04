from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.backend.database.configure import get_db
from src.backend.schemas.user import UserCreate, UserResponse
from src.backend.crud.user import create_user, get_all_users, get_user_by_id, update_user, delete_user

router = APIRouter()

# GET all users
@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# GET user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# POST create a new user
@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.name, user.email)

# PUT update user details
@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, name=user.name, email=user.email)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# DELETE user
@router.delete("/{user_id}", response_model=UserResponse)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
