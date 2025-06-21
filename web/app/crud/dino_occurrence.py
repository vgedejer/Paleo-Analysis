from sqlalchemy.orm import Session
from models.dino_occurrence import DinoFossil

def get_all_fossils(db: Session):
    return db.query(DinoFossil).all()

def get_fossil(db: Session, fossil: str):
    return db.query(DinoFossil).filter(DinoFossil.Fossil == fossil)

def get_fossil_by_id(db: Session, fossil_id: int):
    return db.query(DinoFossil).filter(DinoFossil.index == fossil_id).first()

def get_fossil_by_genus(db: Session, genus: str):
    return db.query(DinoFossil).filter(DinoFossil.Fossil.contains(genus)).all()