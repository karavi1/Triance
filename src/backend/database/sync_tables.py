import os
from dotenv import load_dotenv
from src.backend.database.configure import Base, engine
from src.backend.models.auth_user import AuthUser
from src.backend.models.exercise import Exercise
from src.backend.models.workout import Workout
from src.backend.models.logged_exercise import LoggedExercise
from src.backend.models.logged_exercise_set import LoggedExerciseSet


def sync_tables():
    """Drop and recreate all tables against the configured database."""
    Base.metadata.drop_all(bind=engine)
    print("Dropped all tables.")
    Base.metadata.create_all(bind=engine)
    print("Tables synced successfully.")


if __name__ == "__main__":
    load_dotenv()
    if os.getenv("TESTING", "0") != "1":
        confirm = input("This will DROP ALL TABLES in the database. Type 'yes' to continue: ")
        if confirm.lower() != "yes":
            print("Aborted.")
            exit()
    sync_tables()
