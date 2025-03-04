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

@pytest.fixture(scope="function")
def db_session():
    """Set up a new database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

# Test: Create an Exercise
def test_create_exercise(db_session):
    exercise = create_exercise(db_session, "Push-up", ["chest", "triceps"])
    assert exercise.id is not None
    assert exercise.name == "Push-up"
    assert exercise.body_parts == ["chest", "triceps"]

# Test: Get Exercise by ID
def test_get_exercise_by_id(db_session):
    exercise = create_exercise(db_session, "Squat", ["legs", "glutes"])
    fetched_exercise = get_exercise_by_id(db_session, exercise.id)
    assert fetched_exercise is not None
    assert fetched_exercise.name == "Squat"

# Test: Get All Exercises
def test_get_all_exercises(db_session):
    create_exercise(db_session, "Bench Press", ["chest", "triceps"])
    create_exercise(db_session, "Deadlift", ["back", "legs"])
    exercises = get_all_exercises(db_session)
    assert len(exercises) == 2

# Test: Update Exercise
def test_update_exercise(db_session):
    exercise = create_exercise(db_session, "Plank", ["core"])
    updated_exercise = update_exercise(db_session, exercise.id, body_parts=["core", "shoulders"])
    assert updated_exercise.body_parts == ["core", "shoulders"]

# Test: Delete Exercise
def test_delete_exercise(db_session):
    exercise = create_exercise(db_session, "Lunges", ["legs", "glutes"])
    assert delete_exercise(db_session, exercise.id) is not None
    assert get_exercise_by_id(db_session, exercise.id) is None