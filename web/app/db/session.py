from __future__ import annotations
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from core.config import settings

_is_sqlite = settings.database_url.startswith("sqlite")

if _is_sqlite:
    _connect_args = {"check_same_thread": settings.sqlite_check_same_thread}
else:
    # psycopg3 opens server-side prepared statements by default, which the
    # Supabase transaction pooler (pgbouncer) does not support. Disabling them
    # keeps us safe whether we connect through the pooler or directly.
    _connect_args = {"prepare_threshold": None}

engine = create_engine(
    settings.database_url,
    connect_args=_connect_args,
    # Validate a pooled connection before use so a dropped/recycled Postgres
    # connection is transparently replaced instead of erroring the first request.
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
