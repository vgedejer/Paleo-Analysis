from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from models.genus import Genus


def list_all(db: Session) -> list[Genus]:
    return db.query(Genus).all()


def get_by_id(db: Session, genus_id: int) -> Optional[Genus]:
    return db.query(Genus).filter(Genus.id == genus_id).first()


def get_by_name(db: Session, name: str) -> Optional[Genus]:
    return db.query(Genus).filter(Genus.Genus == name).first()
