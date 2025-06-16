from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.dino_species import DinoSpecies
from schema.dino_species import DinoSpeciesOut
from api.dependencies.db import get_db

router = APIRouter()

#### DINOSAURS ####
@router.get("/dino/all")
def get_all_dino_species(db: Session = Depends(get_db)):
    return db.query(DinoSpecies).all()
