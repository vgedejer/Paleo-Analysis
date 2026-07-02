"""Application configuration.

Replaces the hardcoded `../../paleo.db` path and scattered constants with an
env-driven settings object. Reads from environment variables and falls back to
sensible defaults so local dev still works without a .env file.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load web/.env into the environment before the Settings defaults below are
# evaluated, so PALEO_DATABASE_URL (e.g. the Supabase URL) is picked up in local
# dev. A real env var set by the host still wins — load_dotenv doesn't override
# existing values. config.py → core → app → web, so parents[2] is web/.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _default_db_path() -> str:
    # web/app/core/config.py → web/paleo.db
    here = Path(__file__).resolve()
    return str(here.parents[2] / "paleo.db")


@dataclass(frozen=True)
class Settings:
    app_name: str = "Paleo-Analysis API"
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: str = os.environ.get(
        "PALEO_DATABASE_URL",
        f"sqlite:///{_default_db_path()}",
    )
    sqlite_check_same_thread: bool = False


settings = Settings()
