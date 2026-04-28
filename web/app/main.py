"""FastAPI entry point.

Thin composition root: create app, mount v1 router, install central
exception handlers.
"""
from fastapi import FastAPI

from api.v1 import api_router
from core.config import settings
from core.exceptions import register_exception_handlers

app = FastAPI(title=settings.app_name)

register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "🦕 Welcome to the Mesozoic Era! 🦖"}
