import pytest
from uuid import uuid4
from src.backend.crud import logged_exercise as crud_log
from src.backend.schemas.logged_exercise import LoggedExerciseCreate
from src.backend.schemas.exercise import ExerciseCreate
from src.backend.schemas.user import UserCreate
from src.backend.crud import user as crud_user
from src.backend.crud import exercise as crud_exercise
from src.backend.crud import workout as crud_workout
from src.backend.schemas.workout import WorkoutCreateSimple

def test_log_exercise_and_fetch(db):
    # Set up: create user, exercise, workout
    user = crud_user.create_user(db, UserCreate(email="log@example.com", username="loguser"))
    ex = crud_exercise.create_exercise(db, ExerciseCreate(name="Squat", primary_muscles=["legs"]))

    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username="loguser",
        logged_exercises=[{
            "name": "Squat",
            "sets": 3,
            "reps": 5,
            "weight": 100.0
        }]
    ))

    # Create another logged exercise manually
    log = crud_log.log_exercise(db, LoggedExerciseCreate(
        exercise_id=ex.id,
        sets=4,
        reps=6,
        weight=110.0
    ), workout.id)

    assert log.sets == 4
    assert log.weight == 110.0

    logs = crud_log.get_logged_exercises_by_workout(db, workout.id)
    assert len(logs) == 2  # 1 from workout create + 1 from manual log

def test_delete_logged_exercise(db):
    user = crud_user.create_user(db, UserCreate(email="logdel@example.com", username="logdel"))
    crud_exercise.create_exercise(db, ExerciseCreate(name="Bench", primary_muscles=["chest"]))

    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username="logdel",
        logged_exercises=[{
            "name": "Bench",
            "sets": 3,
            "reps": 5,
            "weight": 50.0
        }]
    ))

    log = crud_log.get_logged_exercises_by_workout(db, workout.id)[0]
    deleted = crud_log.delete_logged_exercise(db, workout.id, log.exercise_id)

    assert deleted is True
    assert len(crud_log.get_logged_exercises_by_workout(db, workout.id)) == 0