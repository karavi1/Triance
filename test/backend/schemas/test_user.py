import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError
from src.backend.schemas.user import UserCreate, UserUpdate, UserOut

def test_valid_user_create():
    user = UserCreate(
        email="test@example.com",
        username="testuser"
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"

def test_invalid_email_user_create():
    with pytest.raises(ValidationError):
        UserCreate(
            email="not-an-email",
            username="testuser"
        )

def test_missing_username_user_create():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@example.com"
            # Missing username
        )

def test_valid_user_update():
    user = UserUpdate(
        email="new@example.com",
        username="newuser"
    )
    assert user.email == "new@example.com"
    assert user.username == "newuser"

def test_valid_user_out():
    uid = uuid4()
    now = datetime.utcnow()

    user = UserOut(
        id=uid,
        email="out@example.com",
        username="outuser",
        created_at=now
    )

    assert user.id == uid
    assert user.email == "out@example.com"
    assert user.username == "outuser"
    assert user.created_at == now
