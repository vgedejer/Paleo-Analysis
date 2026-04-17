from __future__ import annotations
from sqlalchemy.orm import Session
from core.constants import INVALID_FLOAT, INVALID_INTEGER, NOT_SPECIFIED
from core.exceptions import ResourceNotFound
from models.fossil import Fossil
from repositories import fossil_repo
from schemas.fossil import FossilDetail, FossilRead


def _to_read(f: Fossil) -> FossilRead:
    return FossilRead(
        id=f.id,
        Fossil=f.Fossil or NOT_SPECIFIED,
        Longitude=f.Longitude if f.Longitude is not None else INVALID_FLOAT,
        Latitude=f.Latitude if f.Latitude is not None else INVALID_FLOAT,
        Formation=f.Formation or NOT_SPECIFIED,
        Country=f.Country or NOT_SPECIFIED,
        State=f.State or NOT_SPECIFIED,
    )


def _to_detail(f: Fossil) -> FossilDetail:
    return FossilDetail(
        id=f.id,
        Fossil=f.Fossil or NOT_SPECIFIED,
        Longitude=f.Longitude if f.Longitude is not None else INVALID_FLOAT,
        Latitude=f.Latitude if f.Latitude is not None else INVALID_FLOAT,
        Formation=f.Formation or NOT_SPECIFIED,
        Country=f.Country or NOT_SPECIFIED,
        State=f.State or NOT_SPECIFIED,
        County=f.County or NOT_SPECIFIED,
        Collection=f.Collection if f.Collection is not None else INVALID_INTEGER,
        GeoComments=f.GeoComments or NOT_SPECIFIED,
        PaleoLongitude=f.PaleoLongitude if f.PaleoLongitude is not None else INVALID_FLOAT,
        PaleoLatitude=f.PaleoLatitude if f.PaleoLatitude is not None else INVALID_FLOAT,
        GeoPlate=f.GeoPlate or NOT_SPECIFIED,
        GeoGroup=f.GeoGroup or NOT_SPECIFIED,
        Member=f.Member or NOT_SPECIFIED,
        PaleoModel=f.PaleoModel or NOT_SPECIFIED,
    )


def list_fossils(db: Session) -> list[FossilRead]:
    return [_to_read(f) for f in fossil_repo.list_all(db)]


def get_fossil_by_id(db: Session, fossil_id: int) -> FossilDetail:
    f = fossil_repo.get_by_id(db, fossil_id)
    if f is None:
        raise ResourceNotFound(f"Fossil with id {fossil_id} not found")
    return _to_detail(f)


def list_fossils_by_species(db: Session, species_name: str) -> list[FossilDetail]:
    rows = fossil_repo.list_by_species(db, species_name)
    if not rows:
        raise ResourceNotFound(f"No fossils found for species {species_name!r}")
    return [_to_detail(f) for f in rows]


def list_fossils_by_genus(db: Session, genus_name: str) -> list[FossilDetail]:
    rows = fossil_repo.list_by_genus(db, genus_name)
    if not rows:
        raise ResourceNotFound(f"No fossils found for genus {genus_name!r}")
    return [_to_detail(f) for f in rows]
