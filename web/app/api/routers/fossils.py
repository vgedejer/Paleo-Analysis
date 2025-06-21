from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schema.dino_occurrence import DinoFossilOut, DinoFossilOutFull
from services import fossils as fossil_service
from api.dependencies.db import get_db

router = APIRouter()

#### DINOSAURS ####
@router.get("/dino/all", response_model=List[DinoFossilOut])
def get_all_dino_fossils(db: Session = Depends(get_db)):
    return fossil_service.get_all_fossils(db)

@router.get("/dino/{fossil}", response_model=List[DinoFossilOutFull])
def get_dino_fossil(fossil: str, db: Session = Depends(get_db)):
    return fossil_service.get_fossil(db, fossil)

@router.get("/dino/id/{fossil_id}", response_model=DinoFossilOutFull | None)
def get_dino_fossil_by_id(fossil_id: int, db: Session = Depends(get_db)):
    return fossil_service.get_fossil_by_id(db, fossil_id)

@router.get("/dino/genus/{genus}", response_model=List[DinoFossilOutFull])
def get_dino_fossil_by_genus(genus: str, db: Session = Depends(get_db)):
    return fossil_service.get_fossil_by_genus(db, genus)

