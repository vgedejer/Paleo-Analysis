from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from models.fossil import Fossil
from models.genus import Genus


def list_all(db: Session) -> list[Fossil]:
    return db.query(Fossil).all()


def get_by_id(db: Session, fossil_id: int) -> Optional[Fossil]:
    return db.query(Fossil).filter(Fossil.id == fossil_id).first()


def list_by_species(db: Session, species_name: str) -> list[Fossil]:
    return db.query(Fossil).filter(Fossil.Fossil == species_name).all()


def list_by_genus(db: Session, genus_name: str) -> list[Fossil]:
    return (
        db.query(Fossil)
        .join(Genus, Fossil.genus)
        .filter(Genus.Genus == genus_name)
        .all()
    )
