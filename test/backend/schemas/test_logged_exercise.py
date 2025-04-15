import pytest
from uuid import uuid4
from pydantic import ValidationError
from src.backend.schemas.logged_exercise import (
    LoggedExerciseCreate,
    LoggedExerciseUpdate,
    LoggedExerciseOut,
    LoggedExerciseCreateByName
)
from src.backend.schemas.logged_exercise_set import (
    LoggedExerciseSetCreate,
    LoggedExerciseSetOut
)
from src.backend.schemas.exercise import ExerciseSummaryOut

# ---------- LoggedExerciseCreate / Update ----------

def test_valid_logged_exercise_create():
    sets = [
        LoggedExerciseSetCreate(set_number=1, reps=10, weight=100.0),
        LoggedExerciseSetCreate(set_number=2, reps=8, weight=110.0),
    ]

    logged = LoggedExerciseCreate(
        exercise_id=uuid4(),
        sets=sets
    )

    assert len(logged.sets) == 2
    assert logged.sets[0].reps == 10

def test_invalid_logged_exercise_set_negative_values():
    with pytest.raises(ValidationError):
        LoggedExerciseCreate(
            exercise_id=uuid4(),
            sets=[
                LoggedExerciseSetCreate(set_number=1, reps=-5, weight=50.0)
            ]
        )
    with pytest.raises(ValidationError):
        LoggedExerciseCreate(
            exercise_id=uuid4(),
            sets=[
                LoggedExerciseSetCreate(set_number=0, reps=5, weight=50.0)
            ]
        )
    with pytest.raises(ValidationError):
        LoggedExerciseCreate(
            exercise_id=uuid4(),
            sets=[
                LoggedExerciseSetCreate(set_number=1, reps=5, weight=-10.0)
            ]
        )

def test_valid_logged_exercise_update():
    updated = LoggedExerciseUpdate(
        exercise_id=uuid4(),
        sets=[
            LoggedExerciseSetCreate(set_number=1, reps=6, weight=60.0)
        ]
    )
    assert updated.sets[0].reps == 6

# ---------- LoggedExerciseCreateByName ----------

def test_valid_logged_exercise_create_by_name():
    sets = [
        LoggedExerciseSetCreate(set_number=1, reps=5, weight=45.0)
    ]

    logged = LoggedExerciseCreateByName(
        name="Overhead Press",
        sets=sets
    )
    assert logged.name == "Overhead Press"
    assert logged.sets[0].weight == 45.0

def test_invalid_logged_exercise_by_name_negative_sets():
    with pytest.raises(ValidationError):
        LoggedExerciseCreateByName(
            name="Curl",
            sets=[
                LoggedExerciseSetCreate(set_number=1, reps=10, weight=-20.0)
            ]
        )

# ---------- LoggedExerciseOut ----------

def test_valid_logged_exercise_out():
    ex_summary = ExerciseSummaryOut(
        id=uuid4(),
        name="Deadlift"
    )

    sets = [
        LoggedExerciseSetOut(
            id=uuid4(),
            logged_exercise_id=uuid4(),
            set_number=1,
            reps=10,
            weight=120.0
        )
    ]

    logged_out = LoggedExerciseOut(
        id=uuid4(),
        workout_id=uuid4(),
        exercise=ex_summary,
        sets=sets
    )

    assert logged_out.exercise.name == "Deadlift"
    assert logged_out.sets[0].weight == 120.0