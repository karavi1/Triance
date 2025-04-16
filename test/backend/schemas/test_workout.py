import pytest
from uuid import uuid4
from datetime import datetime, timezone
from pydantic import ValidationError
from src.backend.models.enums import ExerciseGroup
from src.backend.schemas.workout import (
    WorkoutCreate,
    WorkoutCreateSimple,
    WorkoutUpdate,
    WorkoutOut
)
from src.backend.schemas.logged_exercise import LoggedExerciseOut, LoggedExerciseCreateByName
from src.backend.schemas.logged_exercise_set import LoggedExerciseSetOut, LoggedExerciseSetCreate
from src.backend.schemas.exercise import ExerciseSummaryOut

# ---------- Helpers ----------

def make_logged_exercise_out():
    return LoggedExerciseOut(
        id=uuid4(),
        workout_id=uuid4(),
        exercise=ExerciseSummaryOut(
            id=uuid4(),
            name="Bench Press",
            category=ExerciseGroup.PUSH
        ),
        sets=[
            LoggedExerciseSetOut(
                id=uuid4(),
                logged_exercise_id=uuid4(),
                set_number=1,
                reps=5,
                weight=100.0
            ),
            LoggedExerciseSetOut(
                id=uuid4(),
                logged_exercise_id=uuid4(),
                set_number=2,
                reps=5,
                weight=105.0
            )
        ]
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
        category=ExerciseGroup.PUSH,
        logged_exercises=[
            LoggedExerciseCreateByName(
                name="Incline Press",
                sets=[
                    LoggedExerciseSetCreate(set_number=1, reps=8, weight=50.0),
                    LoggedExerciseSetCreate(set_number=2, reps=6, weight=55.0)
                ]
            )
        ]
    )
    assert workout.username == "kaushik"
    assert workout.logged_exercises[0].name == "Incline Press"
    assert workout.logged_exercises[0].sets[1].weight == 55.0

def test_invalid_workout_create_simple_missing_exercises():
    with pytest.raises(ValidationError):
        WorkoutCreateSimple(
            username="kaushik",
            notes="forgot exercises",
            category=ExerciseGroup.PUSH,
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
        created_time=datetime.now(timezone.utc),
        notes="Leg day",
        workout_type=ExerciseGroup.QUADS,
        logged_exercises=[make_logged_exercise_out()]
    )
    assert workout.notes == "Leg day"
    assert isinstance(workout.created_time, datetime)
    assert isinstance(workout.logged_exercises[0], LoggedExerciseOut)