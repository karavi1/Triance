import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.backend.database.configure import Base
from src.backend.crud.exercise import (
    create_exercise,
    get_exercise_by_id,
    get_all_exercises,
    update_exercise,
    delete_exercise,
)
from src.backend.models.exercise import Exercise

# Create a test database (in-memory for speed)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture to set up and tear down the database
@pytest.fixture(scope="function")
def db_session():
    # Create tables in test DB
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    yield session  # Provide the session to tests

    # Cleanup: Drop all tables after test
    session.close()
    Base.metadata.drop_all(bind=engine)

# Test: Create an Exercise
def test_create_exercise(db_session):
    exercise = create_exercise(db_session, "Squat", ["Legs", "Glutes"])
    assert exercise.id is not None
    assert exercise.name == "Squat"
    assert exercise.body_parts == "Legs,Glutes"

# Test: Get Exercise by ID
def test_get_exercise_by_id(db_session):
    exercise = create_exercise(db_session, "Bench Press", ["Chest", "Triceps"])
    fetched_exercise = get_exercise_by_id(db_session, exercise.id)
    assert fetched_exercise is not None
    assert fetched_exercise.name == "Bench Press"

# Test: Get All Exercises
def test_get_all_exercises(db_session):
    create_exercise(db_session, "Deadlift", ["Back", "Legs"])
    create_exercise(db_session, "Pull-up", ["Back", "Biceps"])
    exercises = get_all_exercises(db_session)
    assert len(exercises) == 2

# Test: Update Exercise
def test_update_exercise(db_session):
    exercise = create_exercise(db_session, "Push-up", ["Chest", "Triceps"])
    updated_exercise = update_exercise(db_session, exercise.id, "Diamond Push-up", ["Chest", "Triceps", "Shoulders"])
    assert updated_exercise.name == "Diamond Push-up"
    assert updated_exercise.body_parts == "Chest,Triceps,Shoulders"

# Test: Delete Exercise
def test_delete_exercise(db_session):
    exercise = create_exercise(db_session, "Lunges", ["Legs", "Glutes"])
    assert delete_exercise(db_session, exercise.id) is not None
    assert get_exercise_by_id(db_session, exercise.id) is None