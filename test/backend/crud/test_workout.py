import pytest
from uuid import uuid4
from src.backend.crud import workout as crud_workout
from src.backend.crud import user as crud_user
from src.backend.crud import exercise as crud_exercise
from src.backend.schemas.user import UserCreate
from src.backend.schemas.exercise import ExerciseCreate
from src.backend.schemas.workout import WorkoutCreateSimple, WorkoutUpdate

def setup_user_and_exercise(db):
    crud_user.create_user(db, UserCreate(email="wktest@example.com", username="wktest"))
    crud_exercise.create_exercise(db, ExerciseCreate(name="Deadlift", primary_muscles=["back"]))

def test_create_and_get_workout(db):
    setup_user_and_exercise(db)
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        notes="Heavy pulls",
        logged_exercises=[{
            "name": "Deadlift",
            "sets": 4,
            "reps": 5,
            "weight": 180.0
        }]
    ))

    assert workout.notes == "Heavy pulls"
    assert len(workout.logged_exercises) == 1

    fetched = crud_workout.get_workout_by_id(db, workout.id)
    assert fetched.id == workout.id

def test_update_workout_notes(db):
    setup_user_and_exercise(db)
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        logged_exercises=[{
            "name": "Deadlift",
            "sets": 3,
            "reps": 6,
            "weight": 150.0
        }]
    ))

    updated = crud_workout.update_workout(db, workout.id, WorkoutUpdate(notes="Updated note"))
    assert updated.notes == "Updated note"

def test_delete_workout(db):
    setup_user_and_exercise(db)
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        logged_exercises=[{
            "name": "Deadlift",
            "sets": 2,
            "reps": 10,
            "weight": 100.0
        }]
    ))

    deleted = crud_workout.delete_workout(db, workout.id)
    assert deleted is True
    assert crud_workout.get_workout_by_id(db, workout.id) is None