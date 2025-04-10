import pytest
from uuid import uuid4

def setup_user_and_exercise(client):
    # Create user
    client.post("/users/", json={
        "email": "workout@example.com",
        "username": "workouter"
    })
    # Create exercise
    client.post("/exercises/", json={
        "name": "Squat",
        "primary_muscles": ["quads", "glutes"]
    })

def test_create_workout(client):
    setup_user_and_exercise(client)

    response = client.post("/workouts/", json={
        "username": "workouter",
        "notes": "Leg day",
        "logged_exercises": [
            {
                "name": "Squat",
                "sets": 4,
                "reps": 8,
                "weight": 100.0
            }
        ]
    })

    assert response.status_code == 200
    data = response.json()

    # Debug fallback if test fails
    assert isinstance(data, dict), f"Unexpected response: {data}"
    assert "logged_exercises" in data, f"Missing 'logged_exercises': {data}"

    logged = data["logged_exercises"]
    assert isinstance(logged, list)
    assert len(logged) == 1

    entry = logged[0]
    assert entry["sets"] == 4
    assert entry["reps"] == 8
    assert entry["weight"] == 100.0

    # Check nested exercise metadata
    assert "exercise" in entry
    assert isinstance(entry["exercise"], dict)
    assert entry["exercise"]["name"] == "Squat"

def test_get_workout_by_id(client):
    setup_user_and_exercise(client)

    create_resp = client.post("/workouts/", json={
        "username": "workouter",
        "notes": "Strength training",
        "logged_exercises": [
            {"name": "Squat", "sets": 3, "reps": 5, "weight": 120.0}
        ]
    })
    workout_id = create_resp.json()["id"]

    response = client.get(f"/workouts/{workout_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == workout_id
    assert data["notes"] == "Strength training"

def test_get_workout_by_id_not_found(client):
    response = client.get(f"/workouts/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Workout not found"

def test_get_all_workouts(client):
    setup_user_and_exercise(client)

    client.post("/workouts/", json={
        "username": "workouter",
        "logged_exercises": [{"name": "Squat", "sets": 3, "reps": 5, "weight": 120.0}]
    })
    client.post("/workouts/", json={
        "username": "workouter",
        "logged_exercises": [{"name": "Squat", "sets": 2, "reps": 10, "weight": 100.0}]
    })

    response = client.get("/workouts/")
    assert response.status_code == 200
    workouts = response.json()
    assert isinstance(workouts, list)
    assert len(workouts) >= 2

def test_delete_workout(client):
    setup_user_and_exercise(client)

    create_resp = client.post("/workouts/", json={
        "username": "workouter",
        "logged_exercises": [{"name": "Squat", "sets": 3, "reps": 5, "weight": 110.0}]
    })
    workout_id = create_resp.json()["id"]

    del_resp = client.delete(f"/workouts/{workout_id}")
    assert del_resp.status_code == 200
    assert del_resp.json() is True

    # Confirm it's deleted
    get_resp = client.get(f"/workouts/{workout_id}")
    assert get_resp.status_code == 404

def test_delete_workout_not_found(client):
    response = client.delete(f"/workouts/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Workout not found"

def test_get_latest_workout(client):
    setup_user_and_exercise(client)

    # Create two workouts to ensure the latest is returned
    client.post("/workouts/", json={
        "username": "workouter",
        "notes": "Earlier workout",
        "logged_exercises": [{"name": "Squat", "sets": 3, "reps": 5, "weight": 100.0}]
    })
    client.post("/workouts/", json={
        "username": "workouter",
        "notes": "Most recent workout",
        "logged_exercises": [{"name": "Squat", "sets": 4, "reps": 6, "weight": 110.0}]
    })

    response = client.get("/workouts/latest/workouter")
    assert response.status_code == 200

    data = response.json()
    assert "notes" in data
    assert data["notes"] == "Most recent workout"
