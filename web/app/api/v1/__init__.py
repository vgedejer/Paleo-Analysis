"""v1 API router aggregation.

`api_router` is the single object mounted by main.py. Each resource lives in
its own module under api/v1/routers/.
"""
from fastapi import APIRouter

from api.v1.routers import fossils, genera, species, users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(genera.router, prefix="/genera", tags=["Genera"])
api_router.include_router(species.router, prefix="/species", tags=["Species"])
api_router.include_router(fossils.router, prefix="/fossils", tags=["Fossils"])
