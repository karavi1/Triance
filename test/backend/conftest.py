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
from src.backend.schemas.auth_user import AuthUserCreate
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
    """Create a default test user in the DB."""
    user = AuthUserCreate(email="wktest@example.com", username="wktest", password="testpass")
    return crud_user.create_user(db, user)


@pytest.fixture
def test_exercise(db):
    """Create a default test exercise."""
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
    """Helper to construct logged_exercise dicts from name and set data."""
    def _make(name, weights):
        return {
            "name": name,
            "sets": [
                {"set_number": i + 1, "reps": reps, "weight": weight}
                for i, (reps, weight) in enumerate(weights)
            ]
        }
    return _make


@pytest.fixture
def setup_user_and_exercise_api(client):
    """Create a user and optionally a corresponding exercise (via API)."""
    def _setup(username="testuser", email="test@example.com", exercise_name="Squat", category="Quads"):
        client.post("/api/users/", json={"email": email, "username": username, "password": "password"})

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
    """Create user, exercise, and a workout with one logged entry via API."""
    def _setup(username="logapiuser", email="logapi@example.com", exercise_name="Row", category="Pull"):
        client.post("/api/users/", json={"email": email, "username": username, "password": "password"})

        existing_exercises = client.get("/api/exercises/").json()
        if not any(e["name"] == exercise_name for e in existing_exercises):
            client.post("/api/exercises/", json={
                "name": exercise_name,
                "primary_muscles": ["back"],
                "category": category
            })

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
    """Create user via public API."""
    def _create(username="apiuser", email="apiuser@example.com", password="secret123"):
        response = client.post("/api/users/", json={
            "email": email,
            "username": username,
            "password": password
        })
        assert response.status_code == 200
        return response.json()
    return _create


@pytest.fixture
def create_user(db):
    """Create user directly using AuthUserCreate + DB session."""
    def _create(username="testuser", email="test@example.com", password="secret123"):
        user_in = AuthUserCreate(username=username, email=email, password=password)
        return crud_user.create_user(db, user_in)
    return _create


@pytest.fixture
def auth_headers(client, create_user_api):
    """Generate headers with JWT bearer token for a new user."""
    def _auth_headers(username="kaush", password="secret"):
        create_user_api(username=username, email=f"{username}@example.com", password=password)
        response = client.post("/api/users/token", data={"username": username, "password": password})
        assert response.status_code == 200
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return _auth_headers