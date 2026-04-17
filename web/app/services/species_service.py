from __future__ import annotations
from sqlalchemy.orm import Session
from core.constants import NOT_SPECIFIED
from core.exceptions import ResourceNotFound
from models.species import Species
from repositories import species_repo
from schemas.species import SpeciesRead


def _to_read(s: Species) -> SpeciesRead:
    return SpeciesRead(
        id=s.id,
        Species=s.Species or NOT_SPECIFIED,
        Genus=s.Genus or NOT_SPECIFIED,
        Diet=s.Diet or NOT_SPECIFIED,
        EarlyPeriod=s.EarlyPeriod or NOT_SPECIFIED,
        LatePeriod=s.LatePeriod or NOT_SPECIFIED,
    )


def list_species(db: Session) -> list[SpeciesRead]:
    return [_to_read(s) for s in species_repo.list_all(db)]


def get_species_by_id(db: Session, species_id: int) -> SpeciesRead:
    s = species_repo.get_by_id(db, species_id)
    if s is None:
        raise ResourceNotFound(f"Species with id {species_id} not found")
    return _to_read(s)


def get_species_by_name(db: Session, name: str) -> SpeciesRead:
    s = species_repo.get_by_name(db, name)
    if s is None:
        raise ResourceNotFound(f"Species {name!r} not found")
    return _to_read(s)


def list_species_by_genus(db: Session, genus_name: str) -> list[SpeciesRead]:
    rows = species_repo.list_by_genus(db, genus_name)
    if not rows:
        raise ResourceNotFound(f"No species found for genus {genus_name!r}")
    return [_to_read(s) for s in rows]
