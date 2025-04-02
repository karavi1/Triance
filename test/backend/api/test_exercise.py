import pytest
from uuid import UUID, uuid4

def test_create_exercise(client):
    response = client.post("/exercises/", json={
        "name": "Bench Press",
        "primary_muscles": ["chest", "triceps"],
        "secondary_muscles": ["shoulders"],
        "description": "Upper-body compound pressing movement"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bench Press"
    assert "id" in data
    assert isinstance(UUID(data["id"]), UUID)

def test_get_exercise_by_id(client):
    # Create exercise
    response = client.post("/exercises/", json={
        "name": "Squat",
        "primary_muscles": ["quads", "glutes"]
    })
    exercise_id = response.json()["id"]

    # Fetch by ID
    get_response = client.get(f"/exercises/{exercise_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Squat"

def test_get_exercise_by_id_not_found(client):
    response = client.get(f"/exercises/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise not found"

def test_get_all_exercises(client):
    client.post("/exercises/", json={
        "name": "Deadlift",
        "primary_muscles": ["back", "glutes"]
    })
    client.post("/exercises/", json={
        "name": "Overhead Press",
        "primary_muscles": ["shoulders"]
    })

    response = client.get("/exercises/")
    assert response.status_code == 200
    exercises = response.json()
    assert isinstance(exercises, list)
    names = [e["name"] for e in exercises]
    assert "Deadlift" in names
    assert "Overhead Press" in names

def test_delete_exercise(client):
    response = client.post("/exercises/", json={
        "name": "Barbell Row",
        "primary_muscles": ["back"]
    })
    exercise_id = response.json()["id"]

    delete_response = client.delete(f"/exercises/{exercise_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() is True

    # Confirm it's gone
    get_response = client.get(f"/exercises/{exercise_id}")
    assert get_response.status_code == 404

def test_delete_exercise_not_found(client):
    response = client.delete(f"/exercises/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise not found"