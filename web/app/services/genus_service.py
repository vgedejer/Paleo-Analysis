from __future__ import annotations
from sqlalchemy.orm import Session
from core.constants import INVALID_FLOAT, INVALID_INTEGER, NOT_SPECIFIED
from core.exceptions import ResourceNotFound
from models.genus import Genus
from repositories import genus_repo
from schemas.genus import GenusDetail, GenusRead


def _to_read(g: Genus) -> GenusRead:
    return GenusRead(
        id=g.id,
        Genus=g.Genus or NOT_SPECIFIED,
        Family=g.Family or NOT_SPECIFIED,
        Infraorder=g.Infraorder or NOT_SPECIFIED,
        Suborder=g.Suborder or NOT_SPECIFIED,
        Order=g.Order or NOT_SPECIFIED,
        Diet=g.Diet or NOT_SPECIFIED,
        EarlyPeriod=g.EarlyPeriod or NOT_SPECIFIED,
        LatePeriod=g.LatePeriod or NOT_SPECIFIED,
    )


def _to_detail(g: Genus) -> GenusDetail:
    return GenusDetail(
        id=g.id,
        Genus=g.Genus or NOT_SPECIFIED,
        Family=g.Family or NOT_SPECIFIED,
        Infraorder=g.Infraorder or NOT_SPECIFIED,
        Suborder=g.Suborder or NOT_SPECIFIED,
        Order=g.Order or NOT_SPECIFIED,
        Informal=bool(g.Informal) if g.Informal is not None else False,
        TaxonSize=g.TaxonSize if g.TaxonSize is not None else INVALID_INTEGER,
        Diet=g.Diet or NOT_SPECIFIED,
        MaxMYA=g.MaxMYA if g.MaxMYA is not None else INVALID_FLOAT,
        MinMYA=g.MinMYA if g.MinMYA is not None else INVALID_FLOAT,
        LifespanMYA=g.LifespanMYA if g.LifespanMYA is not None else INVALID_FLOAT,
        EarlyAge=g.EarlyAge or NOT_SPECIFIED,
        LateAge=g.LateAge or NOT_SPECIFIED,
        EarlyPeriod=g.EarlyPeriod or NOT_SPECIFIED,
        LatePeriod=g.LatePeriod or NOT_SPECIFIED,
    )


def list_genera(db: Session) -> list[GenusRead]:
    return [_to_read(g) for g in genus_repo.list_all(db)]


def get_genus_by_id(db: Session, genus_id: int, detail: bool = True) -> GenusRead | GenusDetail:
    g = genus_repo.get_by_id(db, genus_id)
    if g is None:
        raise ResourceNotFound(f"Genus with id {genus_id} not found")
    return _to_detail(g) if detail else _to_read(g)


def get_genus_by_name(db: Session, name: str, detail: bool = True) -> GenusRead | GenusDetail:
    g = genus_repo.get_by_name(db, name)
    if g is None:
        raise ResourceNotFound(f"Genus {name!r} not found")
    return _to_detail(g) if detail else _to_read(g)
