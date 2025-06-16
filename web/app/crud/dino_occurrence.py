from sqlalchemy.orm import Session
from models.dino_occurrence import DinoFossil

def get_fossil(db: Session, fossil: str):
    user = db.query(DinoFossil).filter(DinoFossil.Fossil == fossil).first()
    if not user:
        return False
    return user

def get_fossil_by_id(db: Session, fossil_id: int):
    user = db.query(DinoFossil).filter(DinoFossil.index == fossil_id).first()
    if not user:
        return False
    return user