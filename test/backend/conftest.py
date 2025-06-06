import os
os.environ["TESTING"] = "1"

import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.backend.crud import user as crud_user
from src.backend.crud import exercise as crud_exercise
from src.backend.database.configure import Base, get_db
from src.backend.main import app
from src.backend.models.enums import ExerciseGroup
from src.backend.schemas.user import UserCreate
from src.backend.schemas.exercise import ExerciseCreate


def create_temp_db_engine():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    test_database_url = f"sqlite+pysqlite:///{path}"
    engine = create_engine(test_database_url, connect_args={"check_same_thread": False})
    return engine, path

@pytest.fixture(scope="function")
def db():
    engine, db_path = create_temp_db_engine()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists(db_path):
            os.remove(db_path)

@pytest.fixture(scope="function")
def client():
    engine, db_path = create_temp_db_engine()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def test_user(db):
    user = UserCreate(email="wktest@example.com", username="wktest")
    crud_user.create_user(db, user)
    return user

@pytest.fixture
def test_exercise(db):
    exercise = ExerciseCreate(
        name="Deadlift",
        primary_muscles=["back"],
        secondary_muscles=["glutes"],
        description="Posterior chain movement",
        category=ExerciseGroup.PULL
    )
    return crud_exercise.create_exercise(db, exercise)

@pytest.fixture
def make_logged_exercise():
    def _make(name, weights):
        return {
            "name": name,
            "sets": [
                {"set_number": i+1, "reps": reps, "weight": weight}
                for i, (reps, weight) in enumerate(weights)
            ]
        }
    return _make

@pytest.fixture
def setup_user_and_exercise_api(client):
    def _setup(username="testuser", email="test@example.com", exercise_name="Squat", category="Quads"):
        # Create user
        client.post("/api/users/", json={"email": email, "username": username})

        # Check if exercise exists, if not, create
        existing_exercises = client.get("/api/exercises/").json()
        if not any(e["name"] == exercise_name for e in existing_exercises):
            client.post("/api/exercises/", json={
                "name": exercise_name,
                "primary_muscles": ["quads", "glutes"],
                "category": category
            })

        return {
            "username": username,
            "email": email,
            "exercise_name": exercise_name,
            "category": category
        }

    return _setup

@pytest.fixture
def setup_logged_workout_api(client):
    def _setup(username="logapiuser", email="logapi@example.com", exercise_name="Row", category="Pull"):
        # Create user and exercise
        client.post("/api/users/", json={"email": email, "username": username})

        existing_exercises = client.get("/api/exercises/").json()
        if not any(e["name"] == exercise_name for e in existing_exercises):
            client.post("/api/exercises/", json={
                "name": exercise_name,
                "primary_muscles": ["back"],
                "category": category
            })

        # Create a workout with one logged exercise
        resp = client.post("/api/workouts/", json={
            "username": username,
            "notes": "Back day",
            "logged_exercises": [{
                "name": exercise_name,
                "sets": [{"set_number": 1, "reps": 10, "weight": 80.0}]
            }]
        })

        workout_id = resp.json()["id"]
        return {
            "username": username,
            "exercise_name": exercise_name,
            "workout_id": workout_id
        }

    return _setup

@pytest.fixture
def create_user_api(client):
    def _create(username="apiuser", email="apiuser@example.com"):
        response = client.post("/api/users/", json={"email": email, "username": username})
        assert response.status_code == 200
        return response.json()
    return _create

@pytest.fixture
def create_user(db):
    def _create(username="testuser", email="test@example.com"):
        user_in = UserCreate(username=username, email=email)
        return crud_user.create_user(db, user_in)

    return _create