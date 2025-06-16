from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.dino_occurrence import DinoFossil
from schema.dino_occurrence import DinoFossilOut
from crud import dino_occurrence as fossil_crud
from api.dependencies.db import get_db

router = APIRouter()

#### DINOSAURS ####
@router.get("/dino/all")
def get_all_dino_fossils(db: Session = Depends(get_db)):
    return db.query(DinoFossil).all()

@router.get("/dino/{fossil}", response_model=DinoFossilOut)
def get_dino_fossil(fossil: str, db: Session = Depends(get_db)):
    return fossil_crud.get_fossil(db, fossil)

@router.get("/dino/id/{fossil_id}", response_model=DinoFossilOut)
def get_dino_fossil_by_id(fossil_id: int, db: Session = Depends(get_db)):
    return fossil_crud.get_fossil_by_id(db, fossil_id)

