from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.species import SpeciesRead
from services import species_service

router = APIRouter()


@router.get("", response_model=list[SpeciesRead])
def list_species(
    name: str | None = None,
    genus: str | None = None,
    db: Session = Depends(get_db),
) -> list[SpeciesRead]:
    if name is not None:
        return [species_service.get_species_by_name(db, name)]
    if genus is not None:
        return species_service.list_species_by_genus(db, genus)
    return species_service.list_species(db)


@router.get("/{species_id}", response_model=SpeciesRead)
def get_species(species_id: int, db: Session = Depends(get_db)) -> SpeciesRead:
    return species_service.get_species_by_id(db, species_id)
