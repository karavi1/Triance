import pytest
from uuid import uuid4
from src.backend.models.enums import WorkoutType

def setup_user_and_exercise(client, username="workouter", email="workout@example.com", exercise_name="Squat"):
    client.post("/users/", json={"email": email, "username": username})

    existing_exercises = client.get("/exercises/").json()
    if not any(e["name"] == exercise_name for e in existing_exercises):
        client.post("/exercises/", json={
            "name": exercise_name,
            "primary_muscles": ["quads", "glutes"]
        })

def test_create_workout(client):
    setup_user_and_exercise(client)

    response = client.post("/workouts/", json={
        "username": "workouter",
        "notes": "Leg day",
        "logged_exercises": [{
            "name": "Squat",
            "sets": [
                {"set_number": 1, "reps": 8, "weight": 100.0}
            ]
        }]
    })

    assert response.status_code == 201
    data = response.json()
    assert "logged_exercises" in data
    assert isinstance(data["logged_exercises"][0]["sets"], list)

def test_get_workout_by_id(client):
    setup_user_and_exercise(client)

    resp = client.post("/workouts/", json={
        "username": "workouter",
        "notes": "Strength",
        "logged_exercises": [{
            "name": "Squat",
            "sets": [{"set_number": 1, "reps": 5, "weight": 120.0}]
        }]
    })
    workout_id = resp.json()["id"]

    res = client.get(f"/workouts/workout_id/{workout_id}")
    assert res.status_code == 200
    assert res.json()["id"] == workout_id

def test_get_workout_by_id_not_found(client):
    res = client.get(f"/workouts/workout_id/{uuid4()}")
    assert res.status_code == 404
    assert res.json()["detail"] == "Workout not found"

def test_get_all_workouts(client):
    setup_user_and_exercise(client)

    for _ in range(2):
        client.post("/workouts/", json={
            "username": "workouter",
            "logged_exercises": [{
                "name": "Squat",
                "sets": [{"set_number": 1, "reps": 5, "weight": 100.0}]
            }]
        })

    res = client.get("/workouts/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) >= 2

def test_delete_workout(client):
    setup_user_and_exercise(client)

    resp = client.post("/workouts/", json={
        "username": "workouter",
        "logged_exercises": [{
            "name": "Squat",
            "sets": [{"set_number": 1, "reps": 5, "weight": 110.0}]
        }]
    })
    workout_id = resp.json()["id"]

    del_resp = client.delete(f"/workouts/{workout_id}")
    assert del_resp.status_code == 204
    assert del_resp.text == ""  # No content

    get_resp = client.get(f"/workouts/workout_id/{workout_id}")
    assert get_resp.status_code == 404

def test_delete_workout_not_found(client):
    res = client.delete(f"/workouts/{uuid4()}")
    assert res.status_code == 404
    assert res.json()["detail"] == "Workout not found"

def test_get_latest_workout(client):
    setup_user_and_exercise(client)

    client.post("/workouts/", json={
        "username": "workouter",
        "notes": "Earlier workout",
        "logged_exercises": [{
            "name": "Squat",
            "sets": [{"set_number": 1, "reps": 5, "weight": 100.0}]
        }]
    })
    client.post("/workouts/", json={
        "username": "workouter",
        "notes": "Most recent workout",
        "logged_exercises": [{
            "name": "Squat",
            "sets": [{"set_number": 1, "reps": 6, "weight": 110.0}]
        }]
    })

    res = client.get("/workouts/latest/user/workouter")
    assert res.status_code == 200
    assert res.json()["notes"] == "Most recent workout"

def test_api_get_latest_workout_by_type(client):
    setup_user_and_exercise(client, "apitypetester", "apitype@example.com", "Deadlift")

    client.post("/workouts/", json={
        "username": "apitypetester",
        "notes": "Pull workout",
        "workout_type": "Pull",
        "logged_exercises": [{
            "name": "Deadlift",
            "sets": [{"set_number": 1, "reps": 8, "weight": 100.0}]
        }]
    })

    client.post("/workouts/", json={
        "username": "apitypetester",
        "notes": "Latest Pull",
        "workout_type": "Pull",
        "logged_exercises": [{
            "name": "Deadlift",
            "sets": [{"set_number": 1, "reps": 5, "weight": 120.0}]
        }]
    })

    res = client.get("/workouts/apitypetester/latest/Pull")
    assert res.status_code == 200
    assert res.json()["notes"] == "Latest Pull"

def test_api_latest_workout_by_type_none_for_type(client):
    setup_user_and_exercise(client, "apitypetester", "apitype@example.com", "Deadlift")

    client.post("/workouts/", json={
        "username": "apitypetester",
        "notes": "Only Push",
        "workout_type": "Push",
        "logged_exercises": [{
            "name": "Deadlift",
            "sets": [{"set_number": 1, "reps": 10, "weight": 90.0}]
        }]
    })

    res = client.get("/workouts/apitypetester/latest/Pull")
    assert res.status_code == 404
    assert res.json()["detail"] == "No workouts of this type found for this user"

def test_api_latest_workout_by_type_invalid_user(client):
    res = client.get("/workouts/nonexistentuser/latest/Push")
    assert res.status_code == 404
    assert res.json()["detail"] == "No workouts of this type found for this user"

def test_api_latest_workout_by_type_valid_type_other_user(client):
    setup_user_and_exercise(client, "user1", "user1@example.com", "Deadlift")
    setup_user_and_exercise(client, "user2", "user2@example.com", "Deadlift")

    client.post("/workouts/", json={
        "username": "user2",
        "notes": "Quads for user2",
        "workout_type": "Quads",
        "logged_exercises": [{
            "name": "Deadlift",
            "sets": [{"set_number": 1, "reps": 8, "weight": 95.0}]
        }]
    })

    res = client.get("/workouts/user1/latest/Quads")
    assert res.status_code == 404
    assert res.json()["detail"] == "No workouts of this type found for this user"