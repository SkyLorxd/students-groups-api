import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    BigInteger,
    Text,
    ForeignKey,
    text,
)
from sqlalchemy.engine import Engine

load_dotenv()


def build_db_url() -> str:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


engine: Engine = create_engine(build_db_url(), pool_pre_ping=True)

metadata = MetaData()

groups_table = Table(
    "groups",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("group_number", Text, nullable=False, unique=True),
)

students_table = Table(
    "students",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("students_name", Text, nullable=False),
    Column("group_id", BigInteger, ForeignKey("groups.id", ondelete="SET NULL"), nullable=True),
)


def init_db() -> None:
    metadata.create_all(engine)


def fetch_one(stmt, params: dict | None = None):
    with engine.connect() as conn:
        return conn.execute(stmt, params or {}).fetchone()


def fetch_all(stmt, params: dict | None = None):
    with engine.connect() as conn:
        return conn.execute(stmt, params or {}).fetchall()


def execute(stmt, params: dict | None = None) -> int:
    with engine.begin() as conn:
        res = conn.execute(stmt, params or {})
        return res.rowcount
