import os

os.environ["TESTING"] = "1"
os.environ["DB_SECRET_NAME"] = "dummy"

import tempfile
import pytest
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.backend.main import app
from src.backend.database.configure import Base, get_db
from src.backend.crud import user as crud_user
from src.backend.crud import exercise as crud_exercise
from src.backend.schemas.auth_user import AuthUserCreate
from src.backend.schemas.exercise import ExerciseCreate
from src.backend.models.enums import ExerciseGroup
from src.backend.auth.util import get_current_active_user

# Import all models so SQLAlchemy knows about them
from src.backend.models.auth_user import AuthUser
from src.backend.models.exercise import Exercise
from src.backend.models.workout import Workout
from src.backend.models.logged_exercise import LoggedExercise
from src.backend.models.logged_exercise_set import LoggedExerciseSet

# -- Shared test DB engine/path -------------------------------------------
@pytest.fixture(scope="session")
def test_engine_and_path():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    url = f"sqlite+pysqlite:///{path}"
    engine = create_engine(url, connect_args={"check_same_thread": False})
    yield engine, path
    try:
        os.remove(path)
    except OSError:
        pass

# -- DB fixture ------------------------------------------------------------
@pytest.fixture(scope="function")
def db(test_engine_and_path):
    engine, _ = test_engine_and_path
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -- TestClient fixture ---------------------------------------------------
@pytest.fixture(scope="function")
def client(test_engine_and_path):
    engine, _ = test_engine_and_path
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# -- Helper fixtures -------------------------------------------------------
@pytest.fixture
def test_user(db):
    user_in = AuthUserCreate(
        email="wktest@example.com",
        username=f"test_{uuid4().hex[:6]}",
        password="testpass",
    )
    user = crud_user.create_user(db, user_in)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def create_user(db):
    def _create(username="testuser", email="test@example.com", password="secret123", **extra_fields):
        user_in = AuthUserCreate(username=username, email=email, password=password, **extra_fields)
        user = crud_user.create_user(db, user_in)
        db.commit()
        db.refresh(user)
        return user
    return _create

@pytest.fixture
def auth_headers(client):
    def _get_headers(username: str, password: str):
        resp = client.post("/api/users/token", data={"username": username, "password": password})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return _get_headers

@pytest.fixture
def override_current_user(test_user):
    app.dependency_overrides[get_current_active_user] = lambda: test_user
    yield
    app.dependency_overrides.pop(get_current_active_user, None)

@pytest.fixture
def create_user_api(client):
    def _create(username="apiuser", email="apiuser@example.com", password="password"):
        resp = client.post("/api/users/", json={"email": email, "username": username, "password": password})
        assert resp.status_code == 200
        return resp.json()
    return _create

@pytest.fixture
def make_logged_exercise():
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
def setup_user_and_exercise_api(client, override_current_user):
    def _setup(username="testuser", email="test@example.com", exercise_name="Squat", category="Quads"):
        client.post("/api/users/", json={"email": email, "username": username, "password": "password"})
        existing = client.get("/api/exercises/").json()
        if not any(e["name"] == exercise_name for e in existing):
            client.post(
                "/api/exercises/",
                json={
                    "name": exercise_name,
                    "primary_muscles": ["quads", "glutes"],
                    "category": category,
                },
            )
        return {"username": username, "email": email, "exercise_name": exercise_name}
    return _setup

@pytest.fixture
def setup_logged_workout_api(client, override_current_user, setup_user_and_exercise_api, make_logged_exercise):
    def _setup(username="logapiuser", email="logapi@example.com", exercise_name="Row", category="Pull"):
        setup_user_and_exercise_api(username, email, exercise_name, category)
        resp = client.post(
            "/api/workouts/",
            json={
                "username": username,
                "notes": "Back day",
                "logged_exercises": [make_logged_exercise(exercise_name, [(10, 80.0)])],
            },
        )
        data = resp.json()
        return {"username": username, "workout_id": data["id"], "exercise_name": exercise_name}
    return _setup

@pytest.fixture
def test_exercise(db):
    ex = ExerciseCreate(
        name="Deadlift",
        primary_muscles=["back"],
        secondary_muscles=["glutes"],
        description="Posterior chain movement",
        category=ExerciseGroup.PULL,
    )
    return crud_exercise.create_exercise(db, ex, None)