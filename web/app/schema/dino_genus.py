from pydantic import BaseModel

class DinoGenusBase(BaseModel):
    Genus: str
    Family: str
    Infraorder: str
    Suborder: str
    Order: str
    Diet: str
    EarlyPeriod: str
    LatePeriod: str

class DinoGenusCreate(DinoGenusBase):
    pass

class DinoGeneraUpdate(BaseModel):
    Genus: str | None = None
    Family: str | None = None
    Infraorder: str | None = None
    Suborder: str | None = None
    Order: str | None = None
    Informal: int | None = None
    TaxonSize: str | None = None
    Diet: str | None = None
    MaxMYA: int | None = None
    MinMYA: int | None = None
    LifespanMYA: float | None = None
    EarlyAge: str | None = None
    LateAge: str | None = None
    EarlyPeriod: str | None = None
    LatePeriod: str | None = None

class DinoGenusOut(DinoGenusBase):
    index: int

    class Config:
        orm_mode = True