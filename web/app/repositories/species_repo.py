from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from models.species import Species


def list_all(db: Session) -> list[Species]:
    return db.query(Species).all()


def get_by_id(db: Session, species_id: int) -> Optional[Species]:
    return db.query(Species).filter(Species.id == species_id).first()


def get_by_name(db: Session, name: str) -> Optional[Species]:
    return db.query(Species).filter(Species.Species == name).first()


def list_by_genus(db: Session, genus_name: str) -> list[Species]:
    return db.query(Species).filter(Species.Genus == genus_name).all()
