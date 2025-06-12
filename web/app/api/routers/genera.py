from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.dino_genera import DinoGenera
from schema.dino_genera import DinoGeneraBase
from api.dependencies.db import get_db

router = APIRouter()

@router.get("/all")
def get_dino_genera(db: Session = Depends(get_db)):
    return db.query(DinoGenera).all()

@router.get("/{genus}")
def get_dino_genus(genus: str, db: Session = Depends(get_db)):
    dino_genus = db.query(DinoGenera).filter(DinoGenera.Genus == genus).first()
    if not dino_genus:
        return {"error": "Genus not found"}
    return dino_genus