"""Fossils router.

- GET /fossils             (list, optional ?species= or ?genus= filter)
- GET /fossils/{id}
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.fossil import FossilDetail, FossilRead
from services import fossil_service

router = APIRouter()


@router.get("", response_model=list[FossilRead] | list[FossilDetail])
def list_fossils(
    species: str | None = None,
    genus: str | None = None,
    db: Session = Depends(get_db),
) -> list[FossilRead] | list[FossilDetail]:
    if species is not None:
        return fossil_service.list_fossils_by_species(db, species)
    if genus is not None:
        return fossil_service.list_fossils_by_genus(db, genus)
    return fossil_service.list_fossils(db)


@router.get("/{fossil_id}", response_model=FossilDetail)
def get_fossil(fossil_id: int, db: Session = Depends(get_db)) -> FossilDetail:
    return fossil_service.get_fossil_by_id(db, fossil_id)
