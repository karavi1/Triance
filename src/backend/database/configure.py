import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

Base = declarative_base()


def _resolve_database_url() -> str:
    """Resolve the sync DB URL, preferring a plain DATABASE_URL env var.

    Priority:
      1. TESTING=1            -> local SQLite (used by the test suite).
      2. DATABASE_URL set     -> use it directly (e.g. Neon/Postgres or any
                                 standard connection string).
      3. DB_SECRET_NAME set   -> legacy AWS Secrets Manager + RDS fallback.
    """
    if os.getenv("TESTING", "0") == "1":
        return os.getenv("TEST_DATABASE_URL", "sqlite+pysqlite:///:memory:")

    url = os.getenv("DATABASE_URL")
    if url:
        # SQLAlchemy expects "postgresql://"; normalize the "postgres://" alias.
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

    secret_name = os.getenv("DB_SECRET_NAME")
    if secret_name:
        import boto3, json

        client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION", "us-east-2"))
        resp = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(resp["SecretString"])
        username, password = secret["username"], secret["password"]
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "3306")
        name = os.getenv("DB_NAME", "triance")
        return f"mysql+pymysql://{username}:{password}@{host}:{port}/{name}"

    raise RuntimeError(
        "No database configured. Set DATABASE_URL (recommended), or "
        "DB_SECRET_NAME for the legacy AWS Secrets Manager path."
    )


DATABASE_URL = _resolve_database_url()

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()