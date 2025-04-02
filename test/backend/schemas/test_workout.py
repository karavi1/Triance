import pytest
from uuid import uuid4
from datetime import date
from pydantic import ValidationError

from src.backend.schemas.workout import (
    WorkoutCreate,
    WorkoutCreateSimple,
    WorkoutUpdate,
    WorkoutOut
)
from src.backend.schemas.logged_exercise import LoggedExerciseOut, LoggedExerciseCreateByName
from src.backend.schemas.exercise import ExerciseSummaryOut

# ---------- Helpers ----------

def make_logged_exercise_out():
    return LoggedExerciseOut(
        id=uuid4(),
        workout_id=uuid4(),
        sets=3,
        reps=5,
        weight=100.0,
        exercise=ExerciseSummaryOut(
            id=uuid4(),
            name="Bench Press"
        )
    )

# ---------- WorkoutCreate ----------

def test_valid_workout_create():
    workout = WorkoutCreate(
        user_id=uuid4(),
        notes="Upper body focus",
        logged_exercises=[make_logged_exercise_out()]
    )
    assert workout.notes == "Upper body focus"
    assert len(workout.logged_exercises) == 1
    assert isinstance(workout.logged_exercises[0], LoggedExerciseOut)

def test_invalid_workout_create_missing_user_id():
    with pytest.raises(ValidationError):
        WorkoutCreate(
            notes="Bad workout",
            logged_exercises=[make_logged_exercise_out()]
        )

# ---------- WorkoutCreateSimple ----------

def test_valid_workout_create_simple():
    workout = WorkoutCreateSimple(
        username="kaushik",
        notes="Push day",
        logged_exercises=[
            LoggedExerciseCreateByName(
                name="Incline Press",
                sets=3,
                reps=8,
                weight=50.0
            )
        ]
    )
    assert workout.username == "kaushik"
    assert workout.logged_exercises[0].name == "Incline Press"

def test_invalid_workout_create_simple_missing_exercises():
    with pytest.raises(ValidationError):
        WorkoutCreateSimple(
            username="kaushik",
            notes="forgot exercises",
            logged_exercises=[]
        )

# ---------- WorkoutUpdate ----------

def test_workout_update_only_notes():
    update = WorkoutUpdate(notes="Updated notes")
    assert update.notes == "Updated notes"

# ---------- WorkoutOut ----------

def test_valid_workout_out():
    workout = WorkoutOut(
        id=uuid4(),
        user_id=uuid4(),
        workout_date=date.today(),
        notes="Leg day",
        logged_exercises=[make_logged_exercise_out()]
    )
    assert workout.notes == "Leg day"
    assert workout.workout_date == date.today()
    assert isinstance(workout.logged_exercises[0], LoggedExerciseOut)