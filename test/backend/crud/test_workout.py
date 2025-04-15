import pytest
from uuid import uuid4
from src.backend.crud import workout as crud_workout
from src.backend.crud import user as crud_user
from src.backend.crud import exercise as crud_exercise
from src.backend.models.enums import WorkoutType
from src.backend.schemas.user import UserCreate
from src.backend.schemas.exercise import ExerciseCreate
from src.backend.schemas.workout import WorkoutCreateSimple, WorkoutUpdate

def setup_user_and_exercise(db):
    crud_user.create_user(db, UserCreate(email="wktest@example.com", username="wktest"))
    crud_exercise.create_exercise(db, ExerciseCreate(name="Deadlift", primary_muscles=["back"]))

def make_logged_exercise(name, weights):
    return {
        "name": name,
        "sets": [{"set_number": i+1, "reps": reps, "weight": weight} for i, (reps, weight) in enumerate(weights)]
    }

def test_create_and_get_workout(db):
    setup_user_and_exercise(db)
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        notes="Heavy pulls",
        logged_exercises=[make_logged_exercise("Deadlift", [(5, 180.0)])]
    ))

    assert workout.notes == "Heavy pulls"
    assert len(workout.logged_exercises) == 1

    fetched = crud_workout.get_workout_by_workout_id(db, workout.id)
    assert fetched.id == workout.id

def test_update_workout_notes(db):
    setup_user_and_exercise(db)
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        logged_exercises=[make_logged_exercise("Deadlift", [(6, 150.0)])]
    ))

    updated = crud_workout.update_workout(db, workout.id, WorkoutUpdate(notes="Updated note"))
    assert updated.notes == "Updated note"

def test_delete_workout(db):
    setup_user_and_exercise(db)
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        logged_exercises=[make_logged_exercise("Deadlift", [(10, 100.0)])]
    ))

    deleted = crud_workout.delete_workout(db, workout.id)
    assert deleted is True
    assert crud_workout.get_workout_by_workout_id(db, workout.id) is None

def test_get_last_workout(db):
    setup_user_and_exercise(db)

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        notes="First workout",
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 120.0)])]
    ))

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        notes="Second workout",
        logged_exercises=[make_logged_exercise("Deadlift", [(6, 140.0)])]
    ))

    latest = crud_workout.get_last_workout("wktest", db)

    assert latest is not None
    assert latest.notes == "Second workout"
    assert len(latest.logged_exercises) == 1
    assert latest.logged_exercises[0].sets[0].reps == 6

def test_get_last_workout_no_workouts(db):
    crud_user.create_user(db, UserCreate(email="noworkout@example.com", username="noworkout"))
    latest = crud_workout.get_last_workout("noworkout", db)
    assert latest is None

def test_create_workout_with_workout_type(db):
    setup_user_and_exercise(db)
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        notes="Push session",
        workout_type="Push",
        logged_exercises=[make_logged_exercise("Deadlift", [(5, 170.0)])]
    ))

    assert workout.notes == "Push session"
    assert workout.workout_type == WorkoutType.PUSH
    assert len(workout.logged_exercises) == 1

def test_create_workout_without_workout_type(db):
    setup_user_and_exercise(db)
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        notes="Unspecified workout type",
        logged_exercises=[make_logged_exercise("Deadlift", [(10, 135.0)])]
    ))

    assert workout.notes == "Unspecified workout type"
    assert workout.workout_type is None
    assert len(workout.logged_exercises) == 1

def test_get_last_workout_by_type_and_username(db):
    setup_user_and_exercise(db)

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        notes="Push 1",
        workout_type=WorkoutType.PUSH,
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 100.0)])]
    ))

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        notes="Push 2",
        workout_type=WorkoutType.PUSH,
        logged_exercises=[make_logged_exercise("Deadlift", [(6, 120.0)])]
    ))

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        notes="Pull day",
        workout_type=WorkoutType.PULL,
        logged_exercises=[make_logged_exercise("Deadlift", [(5, 130.0)])]
    ))

    result = crud_workout.get_last_workout_based_on_username_and_type("wktest", "Push", db)

    assert result is not None
    assert result.notes == "Push 2"
    assert result.workout_type == WorkoutType.PUSH

def test_get_last_workout_by_type_no_matching_type(db):
    setup_user_and_exercise(db)

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username="wktest",
        notes="Pull day only",
        workout_type=WorkoutType.PULL,
        logged_exercises=[make_logged_exercise("Deadlift", [(10, 100.0)])]
    ))

    result = crud_workout.get_last_workout_based_on_username_and_type("wktest", "Push", db)

    assert result is None

def test_get_last_workout_by_type_for_different_user(db):
    crud_user.create_user(db, UserCreate(email="user1@example.com", username="user1"))
    crud_user.create_user(db, UserCreate(email="user2@example.com", username="user2"))
    crud_exercise.create_exercise(db, ExerciseCreate(name="Deadlift", primary_muscles=["back"]))

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username="user2",
        notes="Quads day for user2",
        workout_type=WorkoutType.QUADS,
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 90.0)])]
    ))

    result = crud_workout.get_last_workout_based_on_username_and_type("user1", "Quads", db)

    assert result is None