from fastapi import HTTPException
from crud import dino_occurrence as fossil_crud
from models.dino_occurrence import DinoFossil
from schema.dino_occurrence import DinoFossilOut, DinoFossilOutFull
from sqlalchemy.orm import Session
import constants

def get_all_fossils(db: Session):
    fossils = fossil_crud.get_all_fossils(db)

    san_fossils = sanitize_fossils(fossils)

    return san_fossils

def get_fossil(db: Session, fossil: str):
    fossils = fossil_crud.get_fossil(db, fossil)

    san_fossils = sanitize_fossils_full(fossils)

    return san_fossils

def get_fossil_by_id(db: Session, fossil_id: int):
    fossil = fossil_crud.get_fossil_by_id(db, fossil_id)

    if fossil is None:
        return HTTPException(status_code=404, detail="Fossil not found")

    purell_fossil = sanitize_fossils_full([fossil])

    return purell_fossil[0]

def get_fossil_by_genus(db: Session, genus: str):
    fossils = fossil_crud.get_fossil_by_genus(db, genus)

    san_fossils = sanitize_fossils_full(fossils)

    return san_fossils

def sanitize_fossils(fossils: list[DinoFossil]):
    purell = []

    for fossil in fossils:
        purell_fossil = DinoFossilOut(
            index=fossil.index,
            Fossil=fossil.Fossil or constants.NOT_SPECIFIED,
            Longitude=fossil.Longitude or constants.INVALID_COORDINATE,
            Latitude=fossil.Latitude or constants.INVALID_COORDINATE,
            Formation=fossil.Formation or constants.NOT_SPECIFIED,
            Country=fossil.Country or constants.NOT_SPECIFIED,
            State=fossil.State or constants.NOT_SPECIFIED,
        )

        purell.append(purell_fossil)

    return purell

def sanitize_fossils_full(fossils: list[DinoFossil]):
    purell = []

    for fossil in fossils:
        purell_fossil = DinoFossilOutFull(
            index=fossil.index,
            Fossil=fossil.Fossil or constants.NOT_SPECIFIED,
            Longitude=fossil.Longitude or constants.INVALID_COORDINATE,
            Latitude=fossil.Latitude or constants.INVALID_COORDINATE,
            Formation=fossil.Formation or constants.NOT_SPECIFIED,
            Country=fossil.Country or constants.NOT_SPECIFIED,
            State=fossil.State or constants.NOT_SPECIFIED,
            County=fossil.County or constants.NOT_SPECIFIED,
            Collection=fossil.Collection or constants.INVALID_COLLECTION_NO,
            GeoComments=fossil.GeoComments or constants.NOT_SPECIFIED,
            PaleoLongitude=fossil.PaleoLongitude or constants.INVALID_COORDINATE,
            PaleoLatitude=fossil.PaleoLatitude or constants.INVALID_COORDINATE,
            GeoPlate=fossil.GeoPlate or constants.NOT_SPECIFIED,
            StratGroup=fossil.StratGroup or constants.NOT_SPECIFIED,
            Member=fossil.Member or constants.NOT_SPECIFIED,
            PaleoModel=fossil.PaleoModel or constants.NOT_SPECIFIED
        )

        purell.append(purell_fossil)


    return purell


