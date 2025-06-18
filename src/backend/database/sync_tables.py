import os
import json
import boto3
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.backend.database.configure import Base, get_db_credentials
from src.backend.models.user import User
from src.backend.models.exercise import Exercise
from src.backend.models.workout import Workout
from src.backend.models.logged_exercise import LoggedExercise

load_dotenv()

# Use shared credential loader with fallback
try:
    secrets = get_db_credentials()
except Exception as e:
    if os.getenv("TESTING", "0") == "1":
        secrets = {"username": "test_user", "password": "test_pass"}
    else:
        raise RuntimeError(f"Failed to load DB credentials: {e}")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "triance")

DATABASE_URL = (
    f"mysql+pymysql://{secrets['username']}:{secrets['password']}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# Drop and recreate all tables
Base.metadata.drop_all(bind=engine)
print("Dropped all tables.")

Base.metadata.create_all(bind=engine)
print("Tables synced successfully!")