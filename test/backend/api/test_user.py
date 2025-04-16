import pytest
from uuid import UUID, uuid4

def test_create_user(client, create_user_api):
    data = create_user_api(username="apiuser", email="apiuser@example.com")
    
    assert isinstance(data, dict)
    assert data["email"] == "apiuser@example.com"
    assert data["username"] == "apiuser"
    assert "id" in data
    assert isinstance(UUID(data["id"]), UUID)

def test_get_user_by_id(client, create_user_api):
    user = create_user_api(username="lookup", email="lookup@example.com")
    user_id = user["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "lookup"
    assert data["email"] == "lookup@example.com"

def test_get_user_by_id_not_found(client):
    response = client.get(f"/users/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_all_users(client, create_user_api):
    create_user_api(username="a", email="a@example.com")
    create_user_api(username="b", email="b@example.com")

    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    usernames = [u["username"] for u in users]
    assert "a" in usernames
    assert "b" in usernames

def test_delete_user(client, create_user_api):
    user = create_user_api(username="deleteuser", email="delete@example.com")
    user_id = user["id"]

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() is True

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "User not found"