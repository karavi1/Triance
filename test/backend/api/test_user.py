import pytest
from uuid import UUID, uuid4

def test_create_user(client, create_user_api):
    data = create_user_api(username="apiuser", email="apiuser@example.com", password="securepass")
    assert isinstance(data, dict)
    assert data["email"] == "apiuser@example.com"
    assert data["username"] == "apiuser"
    assert "id" in data
    assert isinstance(UUID(data["id"]), UUID)

def test_get_user_by_id(client, create_user_api):
    user = create_user_api(username="lookup", email="lookup@example.com", password="pass123")
    user_id = user["id"]
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "lookup"
    assert data["email"] == "lookup@example.com"

def test_get_user_by_id_not_found(client):
    response = client.get(f"/api/users/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_all_users(client, create_user_api):
    create_user_api(username="a", email="a@example.com", password="a123")
    create_user_api(username="b", email="b@example.com", password="b123")
    response = client.get("/api/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    usernames = [u["username"] for u in users]
    assert "a" in usernames
    assert "b" in usernames

def test_delete_user(client, create_user_api):
    user = create_user_api(username="deleteuser", email="delete@example.com", password="deletepass")
    user_id = user["id"]
    delete_response = client.delete(f"/api/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() is True
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "User not found"

def test_update_user(client, create_user_api):
    user = create_user_api(username="usertoupdate", email="usertoupdate@example.com", password="changepass")
    user_id = user["id"]
    patch_resp = client.patch(f"/api/users/{user_id}", json={
        "email": "updatedemail@example.com",
        "full_name": "Updated Name"
    })
    assert patch_resp.status_code == 200
    assert patch_resp.json()["email"] == "updatedemail@example.com"
    assert patch_resp.json()["full_name"] == "Updated Name"

def test_login_for_access_token(client, create_user_api):
    create_user_api(username="loginuser", email="login@example.com", password="secret123")
    response = client.post("/api/users/token", data={
        "username": "loginuser",
        "password": "secret123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_all_users_authenticated(client, auth_headers, create_user_api):
    create_user_api(username="secureuser", email="secure@example.com", password="mypassword")
    headers = auth_headers(username="secureuser", password="mypassword")
    response = client.get("/api/users/auth/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)