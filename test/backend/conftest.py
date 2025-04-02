import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.backend.database.configure import Base, get_db
from src.backend.main import app
from src.backend.models import user, exercise, workout, logged_exercise

def create_temp_db_engine():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)  # Close the file descriptor immediately
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