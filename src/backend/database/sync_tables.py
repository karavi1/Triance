import os
import json
import boto3
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.backend.database.configure import Base
from src.backend.models.user import User
from src.backend.models.exercise import Exercise
from src.backend.models.workout import Workout
from src.backend.models.logged_exercise import LoggedExercise

load_dotenv()

def get_db_credentials():
    secret_name = os.getenv("DB_SECRET_NAME")
    region_name = os.getenv("AWS_REGION", "us-east-2")

    if not secret_name:
        raise ValueError("DB_SECRET_NAME environment variable is required.")

    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])

    return {
        "username": secret["username"],
        "password": secret["password"]
    }

secrets = get_db_credentials()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

if not DB_NAME:
    raise ValueError("DB_NAME must be set in the environment.")

DATABASE_URL = (
    f"mysql+pymysql://{secrets['username']}:{secrets['password']}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

Base.metadata.drop_all(bind=engine)
print("Dropped all tables.")

Base.metadata.create_all(bind=engine)
print("Tables synced successfully!")