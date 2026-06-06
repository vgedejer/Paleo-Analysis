"""Genera router.

- GET /genera              (list, optional ?name= filter, returns GenusRead)
- GET /genera/{id}         (detail=full by default, ?detail=basic shrinks it)
"""
from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.genus import GenusDetail, GenusRead
from services import genus_service

router = APIRouter()

DetailLevel = Literal["basic", "full"]


@router.get("", response_model=list[GenusRead])
def list_genera(
    name: str | None = None,
    detail: DetailLevel = "full",
    db: Session = Depends(get_db),
) -> list[GenusRead]:
    if name is not None:
        return [genus_service.get_genus_by_name(db, name, detail=(detail == "full"))]
    return genus_service.list_genera(db)


@router.get("/{genus_id}", response_model=GenusDetail | GenusRead)
def get_genus(
    genus_id: int,
    detail: DetailLevel = "full",
    db: Session = Depends(get_db),
) -> GenusDetail | GenusRead:
    return genus_service.get_genus_by_id(db, genus_id, detail=(detail == "full"))
