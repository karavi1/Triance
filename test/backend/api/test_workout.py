import pytest
from uuid import uuid4

def make_workout_payload(username="testuser", notes="Leg day", exercise_name="Squat", wt_type="Push", sets=None, created_time=None):
    payload = {
        "username": username,
        "notes": notes,
        "workout_type": wt_type,
        "logged_exercises": [{
            "name": exercise_name,
            "sets": sets or [{"set_number": 1, "reps": 8, "weight": 100.0}]
        }]
    }
    if created_time:
        payload["created_time"] = created_time
    return payload

def test_create_workout(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api()
    response = client.post("/api/workouts/", json=make_workout_payload())
    assert response.status_code == 201
    data = response.json()
    assert "logged_exercises" in data
    assert isinstance(data["logged_exercises"][0]["sets"], list)

def test_get_workout_by_id(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api()
    resp = client.post("/api/workouts/", json=make_workout_payload())
    workout_id = resp.json()["id"]
    res = client.get(f"/api/workouts/{workout_id}")
    assert res.status_code == 200
    assert res.json()["id"] == workout_id

def test_get_workout_by_id_not_found(client):
    res = client.get(f"/api/workouts/{uuid4()}")
    assert res.status_code == 404

def test_get_all_workouts(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api()
    for _ in range(2):
        client.post("/api/workouts/", json=make_workout_payload())
    res = client.get("/api/workouts/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) >= 2

def test_delete_workout(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api()
    resp = client.post("/api/workouts/", json=make_workout_payload())
    workout_id = resp.json()["id"]
    del_resp = client.delete(f"/api/workouts/{workout_id}")
    assert del_resp.status_code == 204
    get_resp = client.get(f"/api/workouts/{workout_id}")
    assert get_resp.status_code == 404

def test_get_latest_workout(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api()
    client.post("/api/workouts/", json=make_workout_payload(notes="Earlier workout"))
    client.post("/api/workouts/", json=make_workout_payload(notes="Most recent workout"))
    res = client.get("/api/workouts/user/testuser/latest")
    assert res.status_code == 200
    assert res.json()["notes"] == "Most recent workout"

def test_api_update_workout(client, setup_user_and_exercise_api):
    setup_user_and_exercise_api(username="patchuser", email="patch@example.com", exercise_name="Deadlift", category="Pull")
    create_resp = client.post("/api/workouts/", json=make_workout_payload(username="patchuser", notes="Initial Workout", exercise_name="Deadlift", wt_type="Pull"))
    workout_id = create_resp.json()["id"]
    update_payload = {
        "notes": "Updated Workout Notes",
        "workout_type": "Push",
        "logged_exercises": [{
            "name": "Deadlift",
            "sets": [{"set_number": 1, "reps": 3, "weight": 140.0}, {"set_number": 2, "reps": 3, "weight": 145.0}]
        }]
    }
    patch_resp = client.patch(f"/api/workouts/{workout_id}", json=update_payload)
    assert patch_resp.status_code == 200
    data = patch_resp.json()
    assert data["notes"] == "Updated Workout Notes"
    assert data["workout_type"] == "Push"
    assert len(data["logged_exercises"]) == 1
    assert len(data["logged_exercises"][0]["sets"]) == 2
    assert data["logged_exercises"][0]["sets"][0]["weight"] == 140.0