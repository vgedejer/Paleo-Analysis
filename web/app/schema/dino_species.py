from pydantic import BaseModel

class DinoSpeciesBase(BaseModel):
    Species: str
    Genus: str
    Diet: str
    EarlyPeriod: str
    LatePeriod: str

class DinoSpeciesCreate(DinoSpeciesBase):
    pass

class DinoSpeciesUpdate(BaseModel):
    Species: str | None = None
    Genus: str | None = None
    Diet: str  | None = None
    MaxMYA: int | None = None
    MinMYA: int | None = None
    LifespanMYA: float | None = None
    EarlyAge: str | None = None
    LateAge: str | None = None
    EarlyPeriod: str | None = None
    LatePeriod: str | None = None

class DinoSpeciesOut(DinoSpeciesBase):
    index: int

    class Config:
        orm_mode = True