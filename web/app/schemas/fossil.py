from __future__ import annotations
from pydantic import BaseModel, ConfigDict


class FossilBase(BaseModel):
    Fossil: str
    Longitude: float
    Latitude: float
    Formation: str
    Country: str
    State: str


class FossilDetailBase(FossilBase):
    County: str
    PaleoLongitude: float
    PaleoLatitude: float
    Collection: int
    GeoComments: str
    GeoPlate: str
    GeoGroup: str
    Member: str
    PaleoModel: str


class FossilCreate(FossilDetailBase):
    pass


class FossilUpdate(BaseModel):
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
    GeoGroup: str | None = None
    Member: str | None = None
    PaleoModel: str | None = None


class FossilRead(FossilBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class FossilDetail(FossilDetailBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
