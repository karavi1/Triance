import pytest
from uuid import uuid4
from src.backend.crud import exercise as crud_exercise
from src.backend.schemas.exercise import ExerciseCreate, ExerciseUpdate
from src.backend.models.enums import ExerciseGroup

def test_create_exercise(db):
    exercise = ExerciseCreate(
        name="Deadlift",
        primary_muscles=["back", "glutes"],
        secondary_muscles=["hamstrings"],
        description="Posterior chain compound lift",
        category=ExerciseGroup.PULL
    )
    created = crud_exercise.create_exercise(db, exercise, None)

    assert created.id is not None
    assert created.name == "Deadlift"
    assert "glutes" in created.primary_muscles

def test_create_batch_exercise(db):
    exercise_1 = ExerciseCreate(
        name="Deadlift",
        primary_muscles=["back", "glutes"],
        secondary_muscles=["hamstrings"],
        description="Posterior chain compound lift",
        category=ExerciseGroup.PULL
    )
    exercise_2 = ExerciseCreate(
        name="Squat",
        primary_muscles=["quads", "glutes"],
        secondary_muscles=["hamstrings"],
        description="Leg compound lift",
        category=ExerciseGroup.QUADS
    )

    created = crud_exercise.create_batch_exercise(db, [exercise_1, exercise_2], None)
    assert created is not None
    assert len(created) == 2
    assert created[0].name == "Deadlift"
    assert created[1].primary_muscles[0] == "quads"

def test_get_exercise_by_id(db):
    created = crud_exercise.create_exercise(
        db,
        ExerciseCreate(
            name="Pull-up",
            primary_muscles=["lats", "biceps"],
            secondary_muscles=["shoulders"],
            description="Bodyweight upper-body pulling movement",
            category=ExerciseGroup.PULL
        ), None
    )
    fetched = crud_exercise.get_exercise_by_id(db, created.id)

    assert fetched.name == "Pull-up"
    assert fetched.id == created.id

def test_get_all_exercises(db):
    crud_exercise.create_exercise(db, ExerciseCreate(
        name="Bench Press",
        primary_muscles=["chest", "triceps"],
        secondary_muscles=["shoulders"],
        category=ExerciseGroup.PUSH
    ), None)
    crud_exercise.create_exercise(db, ExerciseCreate(
        name="Squat",
        primary_muscles=["quads", "glutes"],
        category=ExerciseGroup.QUADS
    ), None)

    all_exercises = crud_exercise.get_all_exercises(db)
    assert len(all_exercises) == 2
    names = [ex.name for ex in all_exercises]
    assert "Bench Press" in names and "Squat" in names

def test_update_exercise(db):
    created = crud_exercise.create_exercise(db, ExerciseCreate(
        name="Row",
        primary_muscles=["back"],
        category=ExerciseGroup.PULL
    ), None)

    updated = crud_exercise.update_exercise(db, created.id, ExerciseUpdate(
        name="Barbell Row",
        primary_muscles=["back", "biceps"]
    ))

    assert updated.name == "Barbell Row"
    assert "biceps" in updated.primary_muscles

def test_update_exercise_invalid_id(db):
    result = crud_exercise.update_exercise(db, uuid4(), ExerciseUpdate(
        name="Invalid Update",
        primary_muscles=["core"]
    ))
    assert result is None

def test_delete_exercise(db):
    created = crud_exercise.create_exercise(db, ExerciseCreate(
        name="Overhead Press",
        primary_muscles=["shoulders"],
        category=ExerciseGroup.PUSH
    ), None)
    deleted = crud_exercise.delete_exercise(db, created.id)

    assert deleted is True
    assert crud_exercise.get_exercise_by_id(db, created.id) is None

def test_delete_exercise_invalid_id(db):
    result = crud_exercise.delete_exercise(db, uuid4())
    assert result is False