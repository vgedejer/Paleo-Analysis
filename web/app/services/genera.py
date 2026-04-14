from fastapi import HTTPException
from crud import dino_genera as genera_crud
from models.dino_genus import DinoGenus
from schema.dino_genus import DinoGenusOut, DinoGenusOutFull
from sqlalchemy.orm import Session
import constants


def get_all_genera(db: Session):
    genera = genera_crud.get_all_genera(db)
    
    if not genera:
        raise HTTPException(status_code=404, detail="...why the fuck is the genus db empty")
    
    san_genera = sanitize_genera(genera)
    
    return san_genera

def get_genera(db: Session, genus: str, basic_info: bool):
    genera = genera_crud.get_genus(db, genus)
    
    if not genera:
        raise HTTPException(status_code=404, detail=f"Genus {genus} not found")
    
    if basic_info:
        san_genera = sanitize_genera([genera])
    else:
        san_genera = sanitize_genera_full([genera])

    return san_genera[0]

def get_genus_by_id(db: Session, genus_id: int, basic_info: bool):
    genus = genera_crud.get_genus_by_id(db, genus_id)

    if not genus:
        raise HTTPException(status_code=404, detail=f"Genus with ID {genus_id} not found")

    if basic_info:
        san_genus = sanitize_genera([genus])
    else:
        san_genus = sanitize_genera_full([genus])

    return san_genus[0]


def sanitize_genera(genera: list[DinoGenus]):
    purell = []
    
    for genus in genera:
        purell_genus = DinoGenusOut(
            index=genus.index,
            Genus=genus.Genus or constants.NOT_SPECIFIED,
            Family=genus.Family or constants.NOT_SPECIFIED,
            Infraorder=genus.Infraorder or constants.NOT_SPECIFIED,
            Suborder=genus.Suborder or constants.NOT_SPECIFIED,
            Order=genus.Order or constants.NOT_SPECIFIED,
            Diet=genus.Diet or constants.NOT_SPECIFIED,
            EarlyPeriod=genus.EarlyPeriod or constants.NOT_SPECIFIED,
            LatePeriod=genus.LatePeriod or constants.NOT_SPECIFIED
        )
        
        purell.append(purell_genus)
        
    return purell
    
def sanitize_genera_full(genera: list[DinoGenus]):
    purell = []
    
    for genus in genera:
        purell_genus = DinoGenusOutFull(
            index=genus.index,
            Genus=genus.Genus,
            Family=genus.Family or constants.NOT_SPECIFIED,
            Infraorder=genus.Infraorder or constants.NOT_SPECIFIED,
            Suborder=genus.Suborder or constants.NOT_SPECIFIED,
            Order=genus.Order or constants.NOT_SPECIFIED,
            Informal=genus.Informal or False,
            TaxonSize=genus.TaxonSize or constants.INVALID_INTEGER,
            Diet=genus.Diet or constants.NOT_SPECIFIED,
            MaxMYA=genus.MaxMYA or constants.INVALID_FLOAT,
            MinMYA=genus.MinMYA or constants.INVALID_FLOAT,
            LifespanMYA=genus.LifespanMYA or constants.INVALID_FLOAT,
            EarlyAge=genus.EarlyAge or constants.NOT_SPECIFIED,
            LateAge=genus.LateAge or constants.NOT_SPECIFIED,
            EarlyPeriod=genus.EarlyPeriod or constants.NOT_SPECIFIED,
            LatePeriod=genus.LatePeriod or constants.NOT_SPECIFIED,
        )
        
        purell.append(purell_genus)
        
    return purell
