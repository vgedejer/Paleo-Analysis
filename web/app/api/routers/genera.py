from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schema.dino_genus import DinoGenusOut
from api.dependencies.db import get_db
from crud import dino_genera as dino_genera_crud

router = APIRouter()

#### DINOSAURS ####
@router.get("/all/dinosaurs")
def get_all_dino_genera(db: Session = Depends(get_db)):
    return dino_genera_crud.get_all_genera(db)

@router.get("/{genus}", response_model=DinoGenusOut)
def get_dino_genus(genus: str, db: Session = Depends(get_db)):
    dino_genus = dino_genera_crud.get_genus(db, genus)
    if not dino_genus:
        raise HTTPException(status_code=404, detail="User not found")
    return dino_genus
