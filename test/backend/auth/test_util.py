import os
import pytest
import jwt
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.backend.database.configure import SessionLocal, Base
from src.backend.models.auth_user import AuthUser
from src.backend.crud import user as crud_user
from src.backend.schemas.auth_user import AuthUserCreate
from src.backend.auth.util import (
    verify_password,
    get_password_hash,
    get_user,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user,
    get_admin_active_user,
    SECRET_KEY,
    ALGORITHM,
)

# Ensure fresh tables before each test function

def setup_function():
    engine = SessionLocal().bind
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_user(db):
    user_in = AuthUserCreate(
        username="testuser",
        email="testuser@example.com",
        password="testpass"
    )
    user = crud_user.create_user(db, user_in)
    db.commit()
    db.refresh(user)
    return user

# Password hashing and verification

def test_password_hash_and_verify():
    password = "mysecret"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)

# User retrieval and authentication

def test_get_user_and_authenticate_user(db, test_user):
    fetched = get_user(db, test_user.username)
    assert fetched.id == test_user.id

    authed = authenticate_user(db, test_user.username, "testpass")
    assert authed and authed.id == test_user.id

    assert authenticate_user(db, test_user.username, "badpass") is None
    assert authenticate_user(db, "nouser", "pass") is None

# JWT creation and decoding

def test_create_access_token_and_decode():
    data = {"sub": "alice"}
    token = create_access_token(data.copy(), expires_delta=timedelta(minutes=1))
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "alice"
    assert "exp" in payload

# Dependency: get_current_user

@pytest.mark.asyncio
async def test_get_current_user_success_and_failure(db, test_user):
    token = create_access_token({"sub": test_user.username}, expires_delta=timedelta(minutes=1))
    user = await get_current_user(token, db)
    assert user.username == test_user.username

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user("invalid.token", db)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED

# Dependency: active and admin user checks

@pytest.mark.asyncio
async def test_get_current_active_user_and_admin(db, test_user):
    # Active user
    active = await get_current_active_user(test_user)
    assert active.id == test_user.id

    # Disabled user
    test_user.disabled = True
    with pytest.raises(HTTPException) as excinfo:
        await get_current_active_user(test_user)
    assert excinfo.value.status_code == status.HTTP_400_BAD_REQUEST

    # Reset and test admin
    test_user.disabled = False
    test_user.is_admin = False
    with pytest.raises(HTTPException) as excinfo2:
        await get_admin_active_user(test_user)
    assert excinfo2.value.status_code == status.HTTP_403_FORBIDDEN

    # Admin user passes
    test_user.is_admin = True
    admin = await get_admin_active_user(test_user)
    assert admin.is_admin