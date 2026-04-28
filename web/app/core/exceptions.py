from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class APIError(Exception):
    """Base class for all domain-level API errors."""

    status_code: int = 500

    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


class ResourceNotFound(APIError):
    status_code = 404


def register_exception_handlers(app: FastAPI) -> None:
    """Register JSON error responses for every APIError subclass."""

    @app.exception_handler(APIError)
    async def _handle_api_error(request: Request, exc: APIError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
