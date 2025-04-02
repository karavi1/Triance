# Simple smoke test

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Fitness Tracker API!"}

def test_custom_docs_endpoint(client):
    response = client.get("/custom-docs")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from the backend!"}