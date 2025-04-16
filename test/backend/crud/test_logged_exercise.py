import pytest
from src.backend.crud import logged_exercise as crud_log
from src.backend.schemas.logged_exercise import LoggedExerciseCreate
from src.backend.schemas.logged_exercise_set import LoggedExerciseSetCreate
from src.backend.crud import workout as crud_workout
from src.backend.schemas.workout import WorkoutCreateSimple


def test_log_exercise_and_fetch(db, test_user, test_exercise, make_logged_exercise):
    # Create workout for the user with one logged exercise
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        logged_exercises=[make_logged_exercise("Deadlift", [(5, 100.0)])]
    ))

    # Log another exercise manually
    log = crud_log.log_exercise(db, LoggedExerciseCreate(
        exercise_id=test_exercise.id,
        sets=[
            LoggedExerciseSetCreate(set_number=1, reps=6, weight=110.0),
            LoggedExerciseSetCreate(set_number=2, reps=5, weight=115.0)
        ]
    ), workout.id)

    assert len(log.sets) == 2
    assert log.sets[0].weight == 110.0

    logs = crud_log.get_logged_exercises_by_workout(db, workout.id)
    assert len(logs) == 2  # 1 from workout creation + 1 manually added


def test_delete_logged_exercise(db, test_user, test_exercise, make_logged_exercise):
    # Create workout with one logged exercise
    workout = crud_workout.create_workout(db, WorkoutCreateSimple(
        username=test_user.username,
        logged_exercises=[make_logged_exercise("Deadlift", [(5, 50.0)])]
    ))

    # Get the first logged exercise
    log = crud_log.get_logged_exercises_by_workout(db, workout.id)[0]

    # Delete it
    deleted = crud_log.delete_logged_exercise(db, workout.id, log.exercise_id)

    assert deleted is True
    assert len(crud_log.get_logged_exercises_by_workout(db, workout.id)) == 0