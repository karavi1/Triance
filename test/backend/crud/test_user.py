import pytest
from uuid import uuid4
from src.backend.crud import user as crud_user
from src.backend.schemas.auth_user import AuthUserCreate, AuthUserUpdate


def test_create_user_default_not_admin(create_user):
    # By default, is_admin should be False
    suffix = str(uuid4())[:8]
    user = create_user(
        username=f"user_{suffix}",
        email=f"user_{suffix}@example.com",
        password="pass123"
    )
    assert user.id is not None
    assert user.email.endswith("@example.com")
    assert user.username.startswith("user_")
    assert user.is_admin is False


def test_create_user_with_admin_flag(create_user):
    suffix = str(uuid4())[:8]
    user = create_user(
        username=f"admin_{suffix}",
        email=f"admin_{suffix}@example.com",
        password="adminpass",
        is_admin=True
    )
    assert user.id is not None
    assert user.is_admin is True


def test_get_user_by_id(db, create_user):
    suffix = str(uuid4())[:8]
    user = create_user(
        username=f"id_{suffix}",
        email=f"id_{suffix}@example.com",
        password="abc123"
    )
    fetched = crud_user.get_user_by_id(db, user.id)
    assert fetched.email == user.email
    assert fetched.id == user.id


def test_get_all_users(db, create_user):
    suffix1 = str(uuid4())[:8]
    suffix2 = str(uuid4())[:8]
    create_user(username=f"u1_{suffix1}", email=f"1_{suffix1}@example.com", password="pass1")
    create_user(username=f"u2_{suffix2}", email=f"2_{suffix2}@example.com", password="pass2", is_admin=True)
    users = crud_user.get_all_users(db)
    emails = [u.email for u in users]
    assert any(e.startswith("1_") for e in emails)
    assert any(e.startswith("2_") for e in emails)


def test_update_user_username_and_admin_flag(db, create_user):
    # Ensure update_user can change both username and is_admin
    suffix = str(uuid4())[:8]
    user = create_user(
        username=f"before_{suffix}",
        email=f"before_{suffix}@example.com",
        password="pass"
    )
    update_data = AuthUserUpdate(username=f"after_{suffix}", is_admin=True)
    updated = crud_user.update_user(db, user.id, update_data)
    assert updated is not None
    assert updated.username == f"after_{suffix}"
    assert updated.is_admin is True


def test_update_user_invalid_id(db):
    result = crud_user.update_user(db, uuid4(), AuthUserUpdate(username="nope"))
    assert result is None


def test_delete_user(db, create_user):
    suffix = str(uuid4())[:8]
    user = create_user(
        username=f"todelete_{suffix}",
        email=f"del_{suffix}@example.com",
        password="delpass"
    )
    result = crud_user.delete_user(db, user.id)
    assert result is True
    assert crud_user.get_user_by_id(db, user.id) is None


def test_delete_user_invalid_id(db):
    result = crud_user.delete_user(db, uuid4())
    assert result is False