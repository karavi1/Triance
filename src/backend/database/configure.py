import os
import json
import boto3
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

def get_db_credentials():
    if os.getenv("TESTING", "0") == "1":
        return {
            "username": "test_user",
            "password": "test_pass"
        }
    
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
DB_NAME = "triance"

DATABASE_URL = (
    f"mysql+pymysql://{secrets['username']}:{secrets['password']}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()