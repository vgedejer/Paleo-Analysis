from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.dino_genus import DinoGenus
from schema.dino_genus import DinoGenusOut
from api.dependencies.db import get_db

router = APIRouter()

#### DINOSAURS ####
@router.get("/dino/all")
def get_all_dino_genera(db: Session = Depends(get_db)):
    return db.query(DinoGenus).all()

@router.get("/dino/{genus}", response_model=DinoGenusOut)
def get_dino_genus(genus: str, db: Session = Depends(get_db)):
    dino_genus = db.query(DinoGenus).filter(DinoGenus.Genus == genus).first()
    if not dino_genus:
        raise HTTPException(status_code=404, detail="User not found")
    return dino_genus
