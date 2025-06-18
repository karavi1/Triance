import pytest
from uuid import uuid4

def test_log_new_exercise(client, setup_logged_workout_api):
    setup = setup_logged_workout_api()
    workout_id = setup["workout_id"]
    ex_resp = client.get("/api/exercises/")
    assert ex_resp.status_code == 200
    exercise_id = ex_resp.json()[0]["id"]
    log_resp = client.post(f"/api/logged_exercises/{workout_id}/log", json={
        "exercise_id": exercise_id,
        "sets": [
            {"set_number": 1, "reps": 6, "weight": 90.0},
            {"set_number": 2, "reps": 6, "weight": 95.0}
        ]
    })
    assert log_resp.status_code == 201
    data = log_resp.json()
    assert data["workout_id"] == workout_id
    assert isinstance(data["sets"], list)
    assert len(data["sets"]) == 2

def test_get_logged_exercises_by_workout(client, setup_logged_workout_api):
    setup = setup_logged_workout_api()
    workout_id = setup["workout_id"]
    response = client.get(f"/api/logged_exercises/{workout_id}/entries")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "sets" in data[0]

def test_delete_logged_exercise(client, setup_logged_workout_api):
    setup = setup_logged_workout_api()
    workout_id = setup["workout_id"]
    log_resp = client.get(f"/api/logged_exercises/{workout_id}/entries")
    exercise_id = log_resp.json()[0]["exercise"]["id"]
    del_resp = client.delete(f"/api/logged_exercises/{workout_id}/entry/{exercise_id}")
    assert del_resp.status_code == 204
    confirm = client.get(f"/api/logged_exercises/{workout_id}/entries")
    assert confirm.status_code == 200
    assert len(confirm.json()) == 0

def test_delete_logged_exercise_not_found(client, setup_logged_workout_api):
    setup = setup_logged_workout_api()
    workout_id = setup["workout_id"]
    fake_exercise_id = str(uuid4())
    response = client.delete(f"/api/logged_exercises/{workout_id}/entry/{fake_exercise_id}")
    assert response.status_code == 404