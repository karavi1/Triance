import os
from dotenv import load_dotenv

load_dotenv()

# If we're running tests, switch to SQLite
if os.getenv("TESTING", "0") == "1":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base

    DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite+pysqlite:///:memory:")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Otherwise, load from AWS Secrets and connect to MySQL
else:
    import boto3, json
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base

    secret_name = os.getenv("DB_SECRET_NAME")
    if not secret_name:
        raise RuntimeError("DB_SECRET_NAME environment variable is required.")

    client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION", "us-east-2"))
    resp = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(resp["SecretString"])
    username, password = secret["username"], secret["password"]

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "triance")
    DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{name}"

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()