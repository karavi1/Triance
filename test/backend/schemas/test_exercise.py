import pytest
from uuid import uuid4
from pydantic import ValidationError
from src.backend.schemas.exercise import (
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseOut,
    ExerciseSummaryOut
)
from src.backend.models.enums import ExerciseGroup

def test_valid_exercise_create():
    exercise = ExerciseCreate(
        name="Bench Press",
        category=ExerciseGroup.PUSH,
        primary_muscles=["chest", "triceps"],
        secondary_muscles=["shoulders"],
        description="A compound upper body exercise."
    )

    assert exercise.name == "Bench Press"
    assert exercise.category == ExerciseGroup.PUSH
    assert "chest" in exercise.primary_muscles
    assert exercise.secondary_muscles == ["shoulders"]

def test_valid_exercise_create_without_optional_fields():
    exercise = ExerciseCreate(
        name="Squat",
        category=ExerciseGroup.QUADS,
        primary_muscles=["quads", "glutes"]
    )

    assert exercise.secondary_muscles is None
    assert exercise.description is None

def test_invalid_exercise_missing_name():
    with pytest.raises(ValidationError):
        ExerciseCreate(
            category=ExerciseGroup.PULL,
            primary_muscles=["back"]
        )

def test_invalid_exercise_missing_primary_muscles():
    with pytest.raises(ValidationError):
        ExerciseCreate(
            name="Row",
            category=ExerciseGroup.PULL
        )

def test_invalid_exercise_missing_category():
    with pytest.raises(ValidationError):
        ExerciseCreate(
            name="Deadlift",
            primary_muscles=["back", "hamstrings"]
        )

def test_valid_exercise_out():
    exercise = ExerciseOut(
        id=uuid4(),
        name="Deadlift",
        category=ExerciseGroup.PULL,
        primary_muscles=["back", "glutes"],
        secondary_muscles=["hamstrings"],
        description="Pulling movement for posterior chain."
    )

    assert exercise.name == "Deadlift"
    assert isinstance(exercise.id, type(uuid4()))
    assert exercise.category == ExerciseGroup.PULL

def test_valid_exercise_summary_out():
    exercise_summary = ExerciseSummaryOut(
        id=uuid4(),
        name="Overhead Press",
        category=ExerciseGroup.PUSH
    )

    assert exercise_summary.name == "Overhead Press"
    assert isinstance(exercise_summary.id, type(uuid4()))
    assert exercise_summary.category == ExerciseGroup.PUSH

def test_valid_exercise_update_partial():
    update = ExerciseUpdate(description="New description only")

    assert update.description == "New description only"
    assert update.name is None

def test_valid_exercise_update_full():
    update = ExerciseUpdate(
        name="Lateral Raise",
        category=ExerciseGroup.PUSH,
        primary_muscles=["shoulders"],
        secondary_muscles=["traps"],
        description="Isolation movement for lateral delts"
    )

    assert update.name == "Lateral Raise"
    assert "shoulders" in update.primary_muscles
    assert update.category == ExerciseGroup.PUSH

def test_invalid_exercise_wrong_type_primary_muscles():
    with pytest.raises(ValidationError):
        ExerciseCreate(
            name="Plank",
            category=ExerciseGroup.PUSH,
            primary_muscles="core"
        )