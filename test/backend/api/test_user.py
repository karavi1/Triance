import pytest
from uuid import UUID

def test_create_user(client):
    response = client.post("/users/", json={
        "email": "apiuser@example.com",
        "username": "apiuser"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "apiuser@example.com"
    assert "id" in data
    assert isinstance(UUID(data["id"]), UUID)

def test_get_user_by_id(client):
    # First, create a user
    response = client.post("/users/", json={
        "email": "lookup@example.com",
        "username": "lookup"
    })
    user_id = response.json()["id"]

    # Then, fetch it
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["username"] == "lookup"

def test_get_user_by_id_not_found(client):
    from uuid import uuid4
    response = client.get(f"/users/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_all_users(client):
    client.post("/users/", json={"email": "a@example.com", "username": "a"})
    client.post("/users/", json={"email": "b@example.com", "username": "b"})

    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert any(u["username"] == "a" for u in users)
    assert any(u["username"] == "b" for u in users)

def test_delete_user(client):
    # Create user
    response = client.post("/users/", json={
        "email": "delete@example.com",
        "username": "deleteuser"
    })
    user_id = response.json()["id"]

    # Delete user
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() is True

    # Confirm deletion
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404