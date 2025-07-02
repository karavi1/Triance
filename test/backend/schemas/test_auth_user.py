import pytest
from uuid import uuid4
from pydantic import ValidationError
from src.backend.schemas.auth_user import (
    AuthUserBase,
    AuthUserCreate,
    AuthUserUpdate,
    AuthUserOut,
    Token,
    TokenData,
)

def test_auth_user_base_valid():
    user = AuthUserBase(username="kaushik", email="k@example.com", full_name="Kaushik R", disabled=False)
    assert user.username == "kaushik"
    assert user.email == "k@example.com"
    assert user.disabled is False
    assert user.is_admin is False


def test_auth_user_base_optional_fields():
    user = AuthUserBase(username="ay")
    assert user.username == "ay"
    assert user.email is None
    assert user.full_name is None
    assert user.disabled is None
    assert user.is_admin is False


def test_auth_user_create_valid():
    user = AuthUserCreate(username="ay", password="secret")
    assert user.password == "secret"
    assert user.username == "ay"
    assert user.is_admin is False


def test_auth_admin_user_create_valid():
    user = AuthUserCreate(username="ay", password="secret", is_admin=True)
    assert user.password == "secret"
    assert user.username == "ay"
    assert user.is_admin is True


def test_auth_user_create_missing_password():
    with pytest.raises(ValidationError):
        AuthUserCreate(username="no_pass")


def test_auth_user_update_fields():
    update = AuthUserUpdate(email="new@example.com", password="newsecret")
    assert update.email == "new@example.com"
    assert update.password == "newsecret"
    assert update.full_name is None


def test_auth_user_out():
    user_id = uuid4()
    user = AuthUserOut(id=user_id, username="ay", email="ay@example.com", full_name="AY", disabled=False)
    assert user.id == user_id
    assert user.username == "ay"
    assert user.disabled is False


def test_token_model():
    token = Token(access_token="abc123", token_type="bearer")
    assert token.access_token == "abc123"
    assert token.token_type == "bearer"

    with pytest.raises(ValidationError):
        Token(access_token="abc123")  # Missing token_type


def test_token_data_model():
    data = TokenData(username="ay")
    assert data.username == "ay"

    empty = TokenData()
    assert empty.username is None