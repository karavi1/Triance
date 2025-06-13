import pytest

# --- Smoke Tests ---

def test_root_endpoint(client):
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Fitness Tracker API!"}

def test_custom_docs_endpoint(client):
    response = client.get("/api/custom-docs")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from the backend!"}

# --- Authentication Tests ---

def test_login_success(client):
    response = client.post("/token", data={"username": "kaush", "password": "secret"})
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"

def test_login_failure(client):
    response = client.post("/token", data={"username": "kaush", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_get_current_user_authenticated(client, auth_headers):
    headers = auth_headers()
    response = client.get("/users/me/", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "kaush"

def test_get_current_user_unauthenticated(client):
    response = client.get("/users/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_items_authenticated(client, auth_headers):
    headers = auth_headers()
    response = client.get("/users/me/items/", headers=headers)
    assert response.status_code == 200
    assert response.json()[0]["owner"] == "kaush"