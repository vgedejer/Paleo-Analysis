from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schema.dino_genus import DinoGenusOut, DinoGenusOutFull
from api.dependencies.db import get_db
from crud import dino_genera as dino_genera_crud
from services import genera as dino_genera_service

router = APIRouter()

#### DINOSAURS ####
@router.get("/all")
def get_all_dino_genera(db: Session = Depends(get_db)):
    return dino_genera_service.get_all_genera(db)

@router.get("/{genus}", response_model=DinoGenusOutFull)
def get_dino_genus(genus: str, db: Session = Depends(get_db)):
    return dino_genera_service.get_genera(db, genus, False)

@router.get("/basic-info/{genus}", response_model=DinoGenusOut)
def get_dino_genus(genus: str, db: Session = Depends(get_db)):
    return dino_genera_service.get_genera(db, genus, True)

@router.get("/id/{genus_id}", response_model=DinoGenusOutFull)
def get_dino_genus_by_id(genus_id: int, db: Session = Depends(get_db)):
    return dino_genera_service.get_genus_by_id(db, genus_id, False)

@router.get("/basic-info/id/{genus_id}", response_model=DinoGenusOut)
def get_dino_genus_by_id(genus_id: int, db: Session = Depends(get_db)):
    return dino_genera_service.get_genus_by_id(db, genus_id, True)


