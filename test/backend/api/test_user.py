import pytest
from uuid import UUID, uuid4

def test_create_user(client, create_user_api):
    suffix = str(uuid4())[:8]
    data = create_user_api(username=f"apiuser_{suffix}", email=f"apiuser_{suffix}@example.com", password="securepass")
    assert isinstance(data, dict)
    assert data["email"].startswith("apiuser_")
    assert "id" in data
    assert isinstance(UUID(data["id"]), UUID)

def test_get_user_by_id(client, create_user_api):
    suffix = str(uuid4())[:8]
    user = create_user_api(username=f"lookup_{suffix}", email=f"lookup_{suffix}@example.com", password="pass123")
    user_id = user["id"]
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"].startswith("lookup_")
    assert data["email"].startswith("lookup_")

def test_get_user_by_id_not_found(client):
    response = client.get(f"/api/users/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_all_users(client, create_user_api):
    suffix1 = str(uuid4())[:8]
    suffix2 = str(uuid4())[:8]
    create_user_api(username=f"usera_{suffix1}", email=f"a_{suffix1}@example.com", password="a123")
    create_user_api(username=f"userb_{suffix2}", email=f"b_{suffix2}@example.com", password="b123")
    response = client.get("/api/users/")
    assert response.status_code == 200
    usernames = [u["username"] for u in response.json()]
    assert any(u.startswith("usera_") for u in usernames)
    assert any(u.startswith("userb_") for u in usernames)

def test_delete_user(client, create_user_api):
    suffix = str(uuid4())[:8]
    user = create_user_api(username=f"delete_{suffix}", email=f"delete_{suffix}@example.com", password="deletepass")
    user_id = user["id"]
    delete_response = client.delete(f"/api/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() is True
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404

def test_update_user(client, create_user_api):
    suffix = str(uuid4())[:8]
    user = create_user_api(username=f"tochange_{suffix}", email=f"tochange_{suffix}@example.com", password="changepass")
    user_id = user["id"]
    patch_resp = client.patch(f"/api/users/{user_id}", json={
        "email": f"updated_{suffix}@example.com",
        "full_name": "Updated Name"
    })
    assert patch_resp.status_code == 200
    assert patch_resp.json()["email"] == f"updated_{suffix}@example.com"
    assert patch_resp.json()["full_name"] == "Updated Name"

def test_login_for_access_token(client, create_user_api):
    suffix = str(uuid4())[:8]
    username = f"login_{suffix}"
    password = "secret123"
    create_user_api(username=username, email=f"{username}@example.com", password=password)
    response = client.post("/api/users/token", data={
        "username": username,
        "password": password
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_all_users_authenticated(client, auth_headers, create_user_api):
    suffix = str(uuid4())[:8]
    username = f"secure_{suffix}"
    password = "mypassword"
    create_user_api(username=username, email=f"{username}@example.com", password=password)
    headers = auth_headers(username=username, password=password)
    response = client.get("/api/users/auth/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)