from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from src.backend.database.configure import get_db
from src.backend.schemas.user import UserCreate, UserUpdate, UserOut
from src.backend.crud.user import (
    create_user,
    get_user_by_id,
    get_all_users,
    delete_user,
    update_user
)

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_200_OK)
def create_user_handler(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.
    """
    return create_user(db, user)

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id_handler(user_id: UUID, db: Session = Depends(get_db)):
    """
    Get a single user by their UUID.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserOut])
def get_all_users_handler(db: Session = Depends(get_db)):
    """
    Get a list of all users.
    """
    return get_all_users(db)

@router.delete("/{user_id}", response_model=bool)
def delete_user_handler(user_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a user by UUID.
    """
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

@router.patch("/{user_id}", response_model=UserOut)
def update_user_handler(user_id: UUID, updates: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user.
    """
    updated = update_user(db, user_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found or not updated")
    return updated