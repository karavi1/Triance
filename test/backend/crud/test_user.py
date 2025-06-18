import pytest
from uuid import uuid4
from src.backend.crud import user as crud_user
from src.backend.schemas.auth_user import AuthUserUpdate

def test_create_user(create_user):
    user = create_user(username="testuser", email="test@example.com", password="pass123")
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.hashed_password is not None

def test_get_user_by_id(db, create_user):
    user = create_user(username="idtest", email="idtest@example.com", password="abc123")
    fetched = crud_user.get_user_by_id(db, user.id)
    assert fetched is not None
    assert fetched.email == "idtest@example.com"
    assert fetched.id == user.id

def test_get_all_users(db, create_user):
    create_user(username="one", email="1@example.com", password="pass1")
    create_user(username="two", email="2@example.com", password="pass2")
    users = crud_user.get_all_users(db)
    assert len(users) >= 2
    emails = [u.email for u in users]
    assert "1@example.com" in emails
    assert "2@example.com" in emails

def test_update_user(db, create_user):
    user = create_user(username="before", email="update@example.com", password="pass")
    update_data = AuthUserUpdate(username="after")
    updated = crud_user.update_user(db, user.id, update_data)
    db.refresh(updated)
    assert updated.username == "after"
    assert updated.id == user.id

def test_update_user_invalid_id(db):
    result = crud_user.update_user(db, uuid4(), AuthUserUpdate(username="nope"))
    assert result is None

def test_delete_user(db, create_user):
    user = create_user(username="todelete", email="delete@example.com", password="delpass")
    result = crud_user.delete_user(db, user.id)
    assert result is True
    assert crud_user.get_user_by_id(db, user.id) is None

def test_delete_user_invalid_id(db):
    result = crud_user.delete_user(db, uuid4())
    assert result is False