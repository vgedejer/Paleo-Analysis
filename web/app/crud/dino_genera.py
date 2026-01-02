from sqlalchemy.orm import Session
from models.dino_genus import DinoGenus

def get_all_genera(db: Session):
    return db.query(DinoGenus).all()

def get_genus(db: Session, genus: str):
    dino_genus = db.query(DinoGenus).filter(DinoGenus.Genus == genus).first()
    if not dino_genus:
        return False
    return dino_genus

def get_genus_by_id(db: Session, genus_id: int):
    dino_genus = db.query(DinoGenus).filter(DinoGenus.ID == genus_id).first()
    if not dino_genus:
        return False
    return dino_genus


