import os
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

load_dotenv()
Base = declarative_base()

# Query params understood by libpq/psycopg2 but NOT by asyncpg; they must be
# stripped from the URL and translated into connect_args instead.
_LIBPQ_ONLY_PARAMS = {"sslmode", "channel_binding"}


def _to_async_url(url: str) -> tuple[str, dict]:
    """Normalize a sync-style URL to an async driver + asyncpg-safe connect_args."""
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    connect_args: dict = {}
    if url.startswith("postgresql+asyncpg://"):
        parts = urlsplit(url)
        kept = [(k, v) for k, v in parse_qsl(parts.query) if k.lower() not in _LIBPQ_ONLY_PARAMS]
        dropped = {k.lower() for k, _ in parse_qsl(parts.query)} & _LIBPQ_ONLY_PARAMS
        # Neon and most managed Postgres require TLS; enable it for asyncpg.
        if "sslmode" in dropped:
            connect_args["ssl"] = True
        url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(kept), parts.fragment))
    return url, connect_args


def _resolve_async_database_url() -> tuple[str, dict]:
    """Resolve the async DB URL, mirroring the sync config's priority order.

    1. TESTING=1          -> local async SQLite.
    2. DATABASE_URL set   -> normalized to an async driver (Postgres -> asyncpg).
    3. DB_SECRET_NAME set -> legacy AWS Secrets Manager + RDS fallback.
    """
    if os.getenv("TESTING", "0") == "1":
        return os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:"), {}

    url = os.getenv("DATABASE_URL")
    if url:
        return _to_async_url(url)

    secret_name = os.getenv("DB_SECRET_NAME")
    if secret_name:
        import json, boto3

        client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION", "us-east-2"))
        resp = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(resp["SecretString"])
        username, password = secret["username"], secret["password"]
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "3306")
        name = os.getenv("DB_NAME", "triance")
        return f"mysql+aiomysql://{username}:{password}@{host}:{port}/{name}", {}

    raise RuntimeError(
        "No database configured. Set DATABASE_URL (recommended), or "
        "DB_SECRET_NAME for the legacy AWS Secrets Manager path."
    )


DATABASE_URL, _connect_args = _resolve_async_database_url()

engine = create_async_engine(DATABASE_URL, echo=False, future=True, connect_args=_connect_args)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session