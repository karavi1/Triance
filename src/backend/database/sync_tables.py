import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.backend.database.configure import Base
from src.backend.models.user import User
from src.backend.models.exercise import Exercise
from src.backend.models.workout import Workout
from src.backend.models.logged_exercise import LoggedExercise

# Load environment variables from .env file
load_dotenv()

# Get DB credentials from .env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construct Database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ✅ Create an engine without 'check_same_thread' (only needed for SQLite)
engine = create_engine(DATABASE_URL)

# Drop all tables (for dev purposes only)
Base.metadata.drop_all(bind=engine)
print("⚠️ Dropped all tables.")

# Recreate all tables
Base.metadata.create_all(bind=engine)
print("✅ Tables synced successfully!")
