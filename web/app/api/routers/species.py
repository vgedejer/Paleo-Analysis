from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.dino_species import DinoSpecies
from schema.dino_species import DinoSpeciesOut
from api.dependencies.db import get_db
from crud import dino_species as dino_species_crud

router = APIRouter()

#### DINOSAURS ####
@router.get("/all")
def get_all_dino_species(db: Session = Depends(get_db)):
    return dino_species_crud.get_all_species(db)

@router.get("/{species}", response_model=DinoSpeciesOut)
def get_dino_species(species: str, db: Session = Depends(get_db)):
    dino_species = dino_species_crud.get_species(db, species)
    if not dino_species:
        raise HTTPException(status_code=404, detail="Species not found")
    return dino_species

@router.get("/genus/{genus}", response_model=list[DinoSpeciesOut])
def get_dino_species_by_genus(genus: str, db: Session = Depends(get_db)):
    dino_species = dino_species_crud.get_species_by_genus(db, genus)
    if not dino_species:
        raise HTTPException(status_code=404, detail="No species found for this genus")
    return dino_species
