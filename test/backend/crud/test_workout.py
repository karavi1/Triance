import pytest
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from src.backend.crud import workout as crud_workout
from src.backend.models.enums import ExerciseGroup
from src.backend.schemas.workout import WorkoutCreateSimple, WorkoutUpdate
from src.backend.schemas.user import UserCreate
from src.backend.schemas.exercise import ExerciseCreate
from src.backend.crud import user as crud_user, exercise as crud_exercise

def test_create_and_get_workout(db, test_user, test_exercise, make_logged_exercise):
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Heavy pulls",
        logged_exercises=[make_logged_exercise("Deadlift", [(5, 180.0)])]
    ))

    assert workout.notes == "Heavy pulls"
    assert len(workout.logged_exercises) == 1

    fetched = crud_workout.get_workout_by_workout_id(db, workout.id)
    assert fetched.id == workout.id

def test_update_workout_notes(db, test_user, test_exercise, make_logged_exercise):
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        logged_exercises=[make_logged_exercise("Deadlift", [(6, 150.0)])]
    ))

    updated = crud_workout.update_workout(db, workout.id, WorkoutUpdate(notes="Updated note"))
    assert updated.notes == "Updated note"

def test_update_workout_logged_exercises(db, test_user, test_exercise, make_logged_exercise):
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        logged_exercises=[make_logged_exercise("Deadlift", [(6, 150.0)])]
    ))

    updated = crud_workout.update_workout(db, workout.id, WorkoutUpdate(logged_exercises=[make_logged_exercise("Deadlift", [(2, 180.0)])]))
    assert updated.logged_exercises is not None
    assert len(updated.logged_exercises) == 1
    assert updated.logged_exercises[0].sets[0].reps == 2
    assert updated.logged_exercises[0].sets[0].weight == 180  

def test_delete_workout(db, test_user, test_exercise, make_logged_exercise):
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        logged_exercises=[make_logged_exercise("Deadlift", [(10, 100.0)])]
    ))

    deleted = crud_workout.delete_workout(db, workout.id)
    assert deleted is True
    assert crud_workout.get_workout_by_workout_id(db, workout.id) is None

def test_get_last_workout(db, test_user, test_exercise, make_logged_exercise):
    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="First workout",
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 120.0)])]
    ))

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Second workout",
        logged_exercises=[make_logged_exercise("Deadlift", [(6, 140.0)])]
    ))

    latest = crud_workout.get_last_workout(test_user.username, db)

    assert latest is not None
    assert latest.notes == "Second workout"
    assert len(latest.logged_exercises) == 1
    assert latest.logged_exercises[0].sets[0].reps == 6

def test_get_last_workout_no_workouts(db):
    crud_user.create_user(db, UserCreate(email="noworkout@example.com", username="noworkout"))
    latest = crud_workout.get_last_workout("noworkout", db)
    assert latest is None

def test_create_workout_with_workout_type(db, test_user, test_exercise, make_logged_exercise):
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Push session",
        workout_type=ExerciseGroup.PUSH,
        logged_exercises=[make_logged_exercise("Deadlift", [(5, 170.0)])]
    ))

    assert workout.notes == "Push session"
    assert workout.workout_type == ExerciseGroup.PUSH
    assert len(workout.logged_exercises) == 1

def test_create_workout_without_workout_type(db, test_user, test_exercise, make_logged_exercise):
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Unspecified workout type",
        logged_exercises=[make_logged_exercise("Deadlift", [(10, 135.0)])]
    ))

    assert workout.notes == "Unspecified workout type"
    assert workout.workout_type is None
    assert len(workout.logged_exercises) == 1

def test_get_last_workout_by_type_and_username(db, test_user, test_exercise, make_logged_exercise):
    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Push 1",
        workout_type=ExerciseGroup.PUSH,
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 100.0)])]
    ))

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Push 2",
        workout_type=ExerciseGroup.PUSH,
        logged_exercises=[make_logged_exercise("Deadlift", [(6, 120.0)])]
    ))

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Pull day",
        workout_type=ExerciseGroup.PULL,
        logged_exercises=[make_logged_exercise("Deadlift", [(5, 130.0)])]
    ))

    result = crud_workout.get_last_workout_based_on_username_and_type(test_user.username, "Push", db)

    assert result is not None
    assert result.notes == "Push 2"
    assert result.workout_type == ExerciseGroup.PUSH

def test_get_last_workout_by_type_no_matching_type(db, test_user, test_exercise, make_logged_exercise):
    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Pull day only",
        workout_type=ExerciseGroup.PULL,
        logged_exercises=[make_logged_exercise("Deadlift", [(10, 100.0)])]
    ))

    result = crud_workout.get_last_workout_based_on_username_and_type(test_user.username, "Push", db)

    assert result is None

def test_get_last_workout_by_type_for_different_user(db, make_logged_exercise):
    # Setup two users
    crud_user.create_user(db, UserCreate(email="user1@example.com", username="user1"))
    crud_user.create_user(db, UserCreate(email="user2@example.com", username="user2"))

    # Add exercise for user2
    crud_exercise.create_exercise(db, ExerciseCreate(
        name="Deadlift",
        primary_muscles=["back"],
        category=ExerciseGroup.PULL
    ))

    # Create workout for user2 only
    crud_workout.create_workout(db, WorkoutCreateSimple(
        username="user2",
        notes="Quads day for user2",
        workout_type=ExerciseGroup.QUADS,
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 90.0)])]
    ))

    result = crud_workout.get_last_workout_based_on_username_and_type("user1", "Quads", db)
    assert result is None


def test_calculate_num_workouts_by_type(db, test_user, test_exercise, make_logged_exercise):
    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Push 1",
        workout_type=ExerciseGroup.PUSH,
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 100.0)])]
    ))

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Push 2",
        workout_type=ExerciseGroup.PUSH,
        logged_exercises=[make_logged_exercise("Deadlift", [(6, 120.0)])]
    ))

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Pull day",
        workout_type=ExerciseGroup.PULL,
        logged_exercises=[make_logged_exercise("Deadlift", [(5, 130.0)])]
    ))

    push_result = crud_workout.calculate_num_workouts_by_type(test_user.username, "Push", db)
    pull_result = crud_workout.calculate_num_workouts_by_type(test_user.username, "Pull", db)
    upper_result = crud_workout.calculate_num_workouts_by_type(test_user.username, "Upper", db)

    assert push_result is 2
    assert pull_result is 1
    assert upper_result is 0

def test_calculate_num_workouts_by_month(db, test_user, test_exercise, make_logged_exercise):
    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Push 1",
        workout_type=ExerciseGroup.PUSH,
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 100.0)])],
        created_time=datetime.now(timezone.utc) - relativedelta(months=2)
    ))
        
    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Pull 1",
        workout_type=ExerciseGroup.PULL,
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 100.0)])],
        created_time=datetime.now(timezone.utc)
    ))

    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Quad 1",
        workout_type=ExerciseGroup.QUADS,
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 100.0)])],
        created_time=datetime.now(timezone.utc) - relativedelta(months=2)
    ))
        
    crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        notes="Ham 1",
        workout_type=ExerciseGroup.HAMS,
        logged_exercises=[make_logged_exercise("Deadlift", [(8, 100.0)])],
        created_time=datetime.now(timezone.utc)
    ))

    result = crud_workout.calculate_num_workouts_by_month(test_user.username, db)
    assert result == 2.0