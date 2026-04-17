"""FastAPI dependencies used by v1 routers.

Kept thin: just re-exports get_db so routers don't reach into db.session
directly. Adds a centralised place to add auth / pagination / rate-limiting
later without touching every router.
"""
from db.session import get_db  # noqa: F401

__all__ = ["get_db"]
