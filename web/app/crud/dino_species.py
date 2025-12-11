from sqlalchemy.orm import Session
from models.dino_species import DinoSpecies

def get_all_species(db: Session):
    return db.query(DinoSpecies).all()

def get_species(db: Session, species: str):
    dino_species = db.query(DinoSpecies).filter(DinoSpecies.Species == species).first()
    if not dino_species:
        return False
    return dino_species

def get_species_by_genus(db: Session, genus: str):
    dino_species = db.query(DinoSpecies).filter(DinoSpecies.Genus == genus).all()
    if not dino_species:
        return False
    return dino_species
