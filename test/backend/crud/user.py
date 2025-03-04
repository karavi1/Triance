import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.backend.database.configure import Base
from src.backend.crud.user import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user,
)
from src.backend.models.user import User

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

# Test: Create a User
def test_create_user(db_session):
    user = create_user(db_session, "John Doe", "johndoe@example.com")
    assert user.user_id is not None
    assert user.name == "John Doe"
    assert user.email == "johndoe@example.com"

# Test: Get User by ID
def test_get_user_by_id(db_session):
    user = create_user(db_session, "Alice", "alice@example.com")
    fetched_user = get_user_by_id(db_session, user.user_id)
    assert fetched_user is not None
    assert fetched_user.name == "Alice"

# Test: Get All Users
def test_get_all_users(db_session):
    create_user(db_session, "Alice", "alice@example.com")
    create_user(db_session, "Bob", "bob@example.com")
    users = get_all_users(db_session)
    assert len(users) == 2

# Test: Update User
def test_update_user(db_session):
    user = create_user(db_session, "Charlie", "charlie@example.com")
    updated_user = update_user(db_session, user.user_id, name="Charlie Updated")
    assert updated_user.name == "Charlie Updated"

# Test: Delete User
def test_delete_user(db_session):
    user = create_user(db_session, "David", "david@example.com")
    assert delete_user(db_session, user.user_id) is True
    assert get_user_by_id(db_session, user.user_id) is None
