import pytest
from uuid import uuid4
from src.backend.crud import user as crud_user
from src.backend.schemas.user import UserCreate, UserUpdate

def test_create_user(db):
    user_data = UserCreate(email="test@example.com", username="testuser")
    user = crud_user.create_user(db, user_data)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"

def test_get_user_by_id(db):
    user_data = UserCreate(email="idtest@example.com", username="idtest")
    user = crud_user.create_user(db, user_data)

    fetched = crud_user.get_user_by_id(db, user.id)
    assert fetched.email == "idtest@example.com"
    assert fetched.id == user.id

def test_get_all_users(db):
    crud_user.create_user(db, UserCreate(email="1@example.com", username="one"))
    crud_user.create_user(db, UserCreate(email="2@example.com", username="two"))

    users = crud_user.get_all_users(db)
    assert len(users) == 2
    emails = [u.email for u in users]
    assert "1@example.com" in emails and "2@example.com" in emails

def test_update_user(db):
    user = crud_user.create_user(db, UserCreate(email="update@example.com", username="before"))
    updated = crud_user.update_user(db, user.id, UserUpdate(email="update@example.com", username="after"))

    assert updated.username == "after"
    assert updated.id == user.id

def test_update_user_invalid_id(db):
    result = crud_user.update_user(db, uuid4(), UserUpdate(username="nope", email="nope@example.com"))
    assert result is None

def test_delete_user(db):
    user = crud_user.create_user(db, UserCreate(email="delete@example.com", username="todelete"))
    result = crud_user.delete_user(db, user.id)

    assert result is True
    assert crud_user.get_user_by_id(db, user.id) is None

def test_delete_user_invalid_id(db):
    result = crud_user.delete_user(db, uuid4())  # random UUID not in DB
    assert result is False