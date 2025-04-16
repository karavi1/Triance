import pytest
from uuid import uuid4

def test_create_workout(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api()

    response = client.post("/workouts/", json={
        "username": "testuser",
        "notes": "Leg day",
        "logged_exercises": [{
            "name": "Squat",
            "sets": [{"set_number": 1, "reps": 8, "weight": 100.0}]
        }]
    })

    assert response.status_code == 201
    data = response.json()
    assert "logged_exercises" in data
    assert isinstance(data["logged_exercises"][0]["sets"], list)

def test_get_workout_by_id(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api()

    resp = client.post("/workouts/", json={
        "username": "testuser",
        "notes": "Strength",
        "logged_exercises": [{
            "name": "Squat",
            "sets": [{"set_number": 1, "reps": 5, "weight": 120.0}]
        }]
    })
    workout_id = resp.json()["id"]

    res = client.get(f"/workouts/{workout_id}")
    assert res.status_code == 200
    assert res.json()["id"] == workout_id

def test_get_workout_by_id_not_found(client):
    res = client.get(f"/workouts/{uuid4()}")
    assert res.status_code == 404
    assert res.json()["detail"] == "Workout not found"

def test_get_all_workouts(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api()

    for _ in range(2):
        client.post("/workouts/", json={
            "username": "testuser",
            "logged_exercises": [{
                "name": "Squat",
                "sets": [{"set_number": 1, "reps": 5, "weight": 100.0}]
            }]
        })

    res = client.get("/workouts/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) >= 2

def test_delete_workout(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api()

    resp = client.post("/workouts/", json={
        "username": "testuser",
        "logged_exercises": [{
            "name": "Squat",
            "sets": [{"set_number": 1, "reps": 5, "weight": 110.0}]
        }]
    })
    workout_id = resp.json()["id"]

    del_resp = client.delete(f"/workouts/{workout_id}")
    assert del_resp.status_code == 204
    assert del_resp.text == ""

    get_resp = client.get(f"/workouts/{workout_id}")
    assert get_resp.status_code == 404

def test_delete_workout_not_found(client):
    res = client.delete(f"/workouts/{uuid4()}")
    assert res.status_code == 404
    assert res.json()["detail"] == "Workout not found"

def test_get_latest_workout(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api()

    client.post("/workouts/", json={
        "username": "testuser",
        "notes": "Earlier workout",
        "logged_exercises": [{
            "name": "Squat",
            "sets": [{"set_number": 1, "reps": 5, "weight": 100.0}]
        }]
    })

    client.post("/workouts/", json={
        "username": "testuser",
        "notes": "Most recent workout",
        "logged_exercises": [{
            "name": "Squat",
            "sets": [{"set_number": 1, "reps": 6, "weight": 110.0}]
        }]
    })

    res = client.get("/workouts/user/testuser/latest")
    assert res.status_code == 200
    assert res.json()["notes"] == "Most recent workout"

def test_api_get_latest_workout_by_type(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api(username="apitypetester", email="apitype@example.com", exercise_name="Deadlift", category="Pull")

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

    res = client.get("/workouts/user/apitypetester/latest/Pull")
    assert res.status_code == 200
    assert res.json()["notes"] == "Latest Pull"

def test_api_latest_workout_by_type_none_for_type(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api(username="apitypetester", email="apitype@example.com", exercise_name="Deadlift", category="Pull")

    client.post("/workouts/", json={
        "username": "apitypetester",
        "notes": "Only Push",
        "workout_type": "Push",
        "logged_exercises": [{
            "name": "Deadlift",
            "sets": [{"set_number": 1, "reps": 10, "weight": 90.0}]
        }]
    })

    res = client.get("/workouts/user/apitypetester/latest/Pull")
    assert res.status_code == 404
    assert res.json()["detail"] == "No workouts of this type found for this user"

def test_api_latest_workout_by_type_invalid_user(client):
    res = client.get("/workouts/user/nonexistentuser/latest/Push")
    assert res.status_code == 404
    assert res.json()["detail"] == "No workouts of this type found for this user"

def test_api_latest_workout_by_type_valid_type_other_user(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api(username="user1", email="user1@example.com", exercise_name="Deadlift", category="Pull")
    setup_user_and_exercise_api(username="user2", email="user2@example.com", exercise_name="Deadlift", category="Pull")

    client.post("/workouts/", json={
        "username": "user2",
        "notes": "Quads for user2",
        "workout_type": "Quads",
        "logged_exercises": [{
            "name": "Deadlift",
            "sets": [{"set_number": 1, "reps": 8, "weight": 95.0}]
        }]
    })

    res = client.get("/workouts/user/user1/latest/Quads")
    assert res.status_code == 404
    assert res.json()["detail"] == "No workouts of this type found for this user"

def test_api_update_workout(client, setup_user_and_exercise_api):
    # Setup: create user + exercise
    setup_user_and_exercise_api(username="patchuser", email="patch@example.com", exercise_name="Deadlift", category="Pull")

    # Create a workout
    create_resp = client.post("/workouts/", json={
        "username": "patchuser",
        "notes": "Initial Workout",
        "workout_type": "Pull",
        "logged_exercises": [
            {
                "name": "Deadlift",
                "sets": [{"set_number": 1, "reps": 5, "weight": 100.0}]
            }
        ]
    })
    assert create_resp.status_code == 201
    workout_id = create_resp.json()["id"]

    # Update the workout
    update_payload = {
        "notes": "Updated Workout Notes",
        "workout_type": "Push",
        "logged_exercises": [
            {
                "name": "Deadlift",
                "sets": [
                    {"set_number": 1, "reps": 3, "weight": 140.0},
                    {"set_number": 2, "reps": 3, "weight": 145.0}
                ]
            }
        ]
    }

    patch_resp = client.patch(f"/workouts/{workout_id}", json=update_payload)
    assert patch_resp.status_code == 200
    data = patch_resp.json()

    # Assertions
    assert data["notes"] == "Updated Workout Notes"
    assert data["workout_type"] == "Push"
    assert len(data["logged_exercises"]) == 1
    assert len(data["logged_exercises"][0]["sets"]) == 2
    assert data["logged_exercises"][0]["sets"][0]["weight"] == 140.0