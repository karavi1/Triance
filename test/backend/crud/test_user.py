import pytest
from uuid import uuid4
from src.backend.crud import user as crud_user
from src.backend.schemas.user import UserUpdate

def test_create_user(create_user):
    user = create_user(username="testuser", email="test@example.com")

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"

def test_get_user_by_id(db, create_user):
    user = create_user(username="idtest", email="idtest@example.com")

    fetched = crud_user.get_user_by_id(db, user.id)
    assert fetched.email == "idtest@example.com"
    assert fetched.id == user.id

def test_get_all_users(create_user):
    create_user(username="one", email="1@example.com")
    create_user(username="two", email="2@example.com")

    users = crud_user.get_all_users(create_user.__closure__[0].cell_contents)
    assert len(users) == 2
    emails = [u.email for u in users]
    assert "1@example.com" in emails and "2@example.com" in emails

def test_update_user(db, create_user):
    user = create_user(username="before", email="update@example.com")
    updated = crud_user.update_user(db, user.id, UserUpdate(username="after", email="update@example.com"))

    assert updated.username == "after"
    assert updated.id == user.id

def test_update_user_invalid_id(db):
    result = crud_user.update_user(db, uuid4(), UserUpdate(username="nope", email="nope@example.com"))
    assert result is None

def test_delete_user(db, create_user):
    user = create_user(username="todelete", email="delete@example.com")
    result = crud_user.delete_user(db, user.id)

    assert result is True
    assert crud_user.get_user_by_id(db, user.id) is None

def test_delete_user_invalid_id(db):
    result = crud_user.delete_user(db, uuid4())
    assert result is False