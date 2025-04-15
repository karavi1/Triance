import pytest
from uuid import uuid4
from pydantic import ValidationError
from src.backend.schemas.logged_exercise_set import (
    LoggedExerciseSetCreate,
    LoggedExerciseSetOut
)

# ---------- LoggedExerciseSetCreate ----------

def test_valid_logged_exercise_set_create():
    set_data = LoggedExerciseSetCreate(
        set_number=1,
        reps=10,
        weight=100.0
    )
    assert set_data.set_number == 1
    assert set_data.reps == 10
    assert set_data.weight == 100.0

def test_invalid_logged_exercise_set_negative_reps():
    with pytest.raises(ValidationError):
        LoggedExerciseSetCreate(
            set_number=1,
            reps=-1,
            weight=100.0
        )

def test_invalid_logged_exercise_set_negative_weight():
    with pytest.raises(ValidationError):
        LoggedExerciseSetCreate(
            set_number=1,
            reps=10,
            weight=-5.0
        )

def test_invalid_logged_exercise_set_zero_set_number():
    with pytest.raises(ValidationError):
        LoggedExerciseSetCreate(
            set_number=0,
            reps=10,
            weight=50.0
        )

# ---------- LoggedExerciseSetOut ----------

def test_valid_logged_exercise_set_out():
    set_out = LoggedExerciseSetOut(
        id=uuid4(),
        logged_exercise_id=uuid4(),
        set_number=2,
        reps=8,
        weight=95.0
    )
    assert isinstance(set_out.id, uuid4().__class__)
    assert isinstance(set_out.logged_exercise_id, uuid4().__class__)
    assert set_out.set_number == 2
    assert set_out.reps == 8
    assert set_out.weight == 95.0