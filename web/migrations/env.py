"""Alembic migration environment.

Wired to the application's own config and model metadata:

* the DB URL comes from `core.config.settings` (which reads PALEO_DATABASE_URL /
  .env), so migrations always target the same DB the app does — no duplicated
  connection string in alembic.ini;
* `target_metadata` is the app's `Base.metadata` with every model imported, so
  `alembic revision --autogenerate` can diff the models against the live schema.
"""
from __future__ import annotations

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Make the app package importable (web/app), mirroring pytest's `pythonpath = app`.
APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from core.config import settings  # noqa: E402
from db.base import Base  # noqa: E402
import models  # noqa: E402,F401  # registers every model on Base.metadata

config = context.config

# Inject the app's DB URL so it never has to live in alembic.ini.
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Emit SQL without a DB connection (`alembic upgrade --sql`)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # detect column type changes, not just add/drop
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against a live DB connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
