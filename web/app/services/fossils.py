from fastapi import HTTPException
from crud import dino_occurrence as fossil_crud
from models.dino_occurrence import DinoFossil
from schema.dino_occurrence import DinoFossilOut, DinoFossilOutFull
from sqlalchemy.orm import Session

def get_all_fossils(db: Session):
    fossils = fossil_crud.get_all_fossils(db)

    san_fossils = sanitize_fossils(fossils)

    return san_fossils

def get_fossil(db: Session, fossil: str):
    fossils = fossil_crud.get_fossil(db, fossil)

    san_fossils = sanitize_fossils(fossils)

    return san_fossils

def get_fossil_by_id(db: Session, fossil_id: int):
    fossil = fossil_crud.get_fossil_by_id(db, fossil_id)

    if fossil is None:
        return HTTPException(status_code=404, detail="Fossil not found")

    purell_fossil = sanitize_fossils([fossil])

    return purell_fossil[0]

def get_fossil_by_genus(db: Session, genus: str):
    fossils = fossil_crud.get_fossil_by_genus(db, genus)

    san_fossils = sanitize_fossils(fossils)

    return san_fossils

def sanitize_fossils(fossils: list[DinoFossil]):
    purell = []

    for fossil in fossils:
        purell_fossil = DinoFossilOut(
            index=fossil.index,
            Fossil=fossil.Fossil or "",
            Longitude=fossil.Longitude or -999.99,
            Latitude=fossil.Latitude or -999.99,
            Formation=fossil.Formation or "",
            Country=fossil.Country or "",
            State=fossil.State or "",
        )

        purell.append(purell_fossil)

    return purell

def sanitize_fossils_full(fossils: list[DinoFossil]):
    purell = []

    for fossil in fossils:
        purell_fossil = DinoFossilOutFull(
            index=fossil.index,
            Fossil=fossil.Fossil or "",
            Longitude=fossil.Longitude or -999.99,
            Latitude=fossil.Latitude or -999.99,
            Formation=fossil.Formation or "",
            Country=fossil.Country or "",
            State=fossil.State or "",
            County=fossil.County or "",
            Collection=fossil.Collection or -999,
            GeoComments=fossil.GeoComments or "",
            PaleoLongitude=fossil.PaleoLongitude or -999.99,
            PaleoLatitude=fossil.PaleoLatitude or -999.99,
            GeoPlate=fossil.GeoPlate or "",
            StratGroup=fossil.StratGroup or "",
            Member=fossil.Member or "",
            PaleoModel=fossil.PaleoModel or ""
        )

        purell.append(purell_fossil)


    return purell


