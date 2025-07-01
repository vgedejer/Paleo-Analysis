from pydantic import BaseModel


class DinoFossilBase(BaseModel):
    Fossil: str
    Longitude: float
    Latitude: float
    Formation: str
    Country: str
    State: str

class DinoFossilExtendedBase(DinoFossilBase):
    County: str
    PaleoLongitude: float
    PaleoLatitude: float
    Collection: int
    GeoComments: str
    GeoPlate: str
    StratGroup: str
    Member: str
    PaleoModel: str

class DinoFossilCreate(DinoFossilExtendedBase):
    pass

class DinoFossilUpdate(BaseModel):
    Fossil: str | None = None
    Longitude: float | None = None
    Latitude: float | None = None
    Formation: str | None = None
    Country: str | None = None
    State: str | None = None
    County: str | None = None
    Collection: int | None = None
    GeoComments: str | None = None
    PaleoLongitude: float | None = None
    PaleoLatitude: float | None = None
    GeoPlate: str | None = None
    StratGroup: str | None = None
    Member: str | None = None
    PaleoModel: str | None = None

class DinoFossilOut(DinoFossilBase):
    index: int

    class Config:
        orm_mode = True


class DinoFossilOutFull(DinoFossilExtendedBase):
    index: int

    class Config:
        orm_mode = True
