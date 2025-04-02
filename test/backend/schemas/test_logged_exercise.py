import pytest
from uuid import uuid4
from pydantic import ValidationError
from src.backend.schemas.logged_exercise import (
    LoggedExerciseCreate,
    LoggedExerciseUpdate,
    LoggedExerciseOut,
    LoggedExerciseCreateByName
)
from src.backend.schemas.exercise import ExerciseSummaryOut

# ---------- LoggedExerciseCreate / Update ----------

def test_valid_logged_exercise_create():
    logged = LoggedExerciseCreate(
        exercise_id=uuid4(),
        sets=4,
        reps=8,
        weight=75.0
    )
    assert logged.sets == 4
    assert logged.reps == 8
    assert logged.weight == 75.0

def test_invalid_logged_exercise_negative_values():
    with pytest.raises(ValidationError):
        LoggedExerciseCreate(
            exercise_id=uuid4(),
            sets=-1,
            reps=5,
            weight=50.0
        )
    with pytest.raises(ValidationError):
        LoggedExerciseCreate(
            exercise_id=uuid4(),
            sets=3,
            reps=-2,
            weight=50.0
        )
    with pytest.raises(ValidationError):
        LoggedExerciseCreate(
            exercise_id=uuid4(),
            sets=3,
            reps=5,
            weight=-10.0
        )

def test_valid_logged_exercise_update():
    updated = LoggedExerciseUpdate(
        exercise_id=uuid4(),
        sets=5,
        reps=5,
        weight=60.0
    )
    assert updated.sets == 5

# ---------- LoggedExerciseCreateByName ----------

def test_valid_logged_exercise_create_by_name():
    logged = LoggedExerciseCreateByName(
        name="Overhead Press",
        sets=3,
        reps=5,
        weight=45.0
    )
    assert logged.name == "Overhead Press"

def test_invalid_logged_exercise_by_name_negative_sets():
    with pytest.raises(ValidationError):
        LoggedExerciseCreateByName(
            name="Curl",
            sets=-3,
            reps=10,
            weight=20.0
        )

# ---------- LoggedExerciseOut ----------

def test_valid_logged_exercise_out():
    ex_summary = ExerciseSummaryOut(
        id=uuid4(),
        name="Deadlift"
    )

    logged_out = LoggedExerciseOut(
        id=uuid4(),
        workout_id=uuid4(),
        sets=3,
        reps=10,
        weight=120.0,
        exercise=ex_summary
    )

    assert logged_out.exercise.name == "Deadlift"
    assert logged_out.sets == 3
    assert logged_out.weight == 120.0
