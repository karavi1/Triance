from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Annotated, List

from src.backend.database.configure import get_db
from src.backend.schemas.auth_user import (
    AuthUserCreate,
    AuthUserUpdate,
    AuthUserOut,
    Token
)
from src.backend.crud.user import (
    create_user,
    get_user_by_id,
    get_user_by_username,
    get_all_users,
    delete_user,
    update_user
)
from src.backend.models.auth_user import AuthUser
from src.backend.auth.util import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user
)

router = APIRouter()

@router.post("/", response_model=AuthUserOut, status_code=status.HTTP_200_OK)
def create_user_handler(user: AuthUserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")
    return create_user(db, user)


@router.get("/{user_id}", response_model=AuthUserOut)
def get_user_by_id_handler(user_id: UUID, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/all/", response_model=List[AuthUserOut])
def get_all_users_handler(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get("/all/auth/", response_model=List[AuthUserOut])
def get_all_users_handler_with_auth(
    _: Annotated[AuthUser, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    return get_all_users(db)


@router.delete("/{user_id}", response_model=bool)
def delete_user_handler(user_id: UUID, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success


@router.patch("/{user_id}", response_model=AuthUserOut)
def update_user_handler(user_id: UUID, updates: AuthUserUpdate, db: Session = Depends(get_db)):
    updated = update_user(db, user_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found or not updated")
    return updated


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")