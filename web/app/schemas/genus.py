from __future__ import annotations
from pydantic import BaseModel, ConfigDict


class GenusBase(BaseModel):
    Genus: str
    Family: str
    Infraorder: str
    Suborder: str
    Order: str
    Diet: str
    EarlyPeriod: str
    LatePeriod: str


class GenusDetailBase(GenusBase):
    Informal: bool
    TaxonSize: int
    MaxMYA: float
    MinMYA: float
    LifespanMYA: float
    EarlyAge: str
    LateAge: str


class GenusCreate(GenusDetailBase):
    pass


class GenusUpdate(BaseModel):
    Genus: str | None = None
    Family: str | None = None
    Infraorder: str | None = None
    Suborder: str | None = None
    Order: str | None = None
    Informal: bool | None = None
    TaxonSize: int | None = None
    Diet: str | None = None
    MaxMYA: float | None = None
    MinMYA: float | None = None
    LifespanMYA: float | None = None
    EarlyAge: str | None = None
    LateAge: str | None = None
    EarlyPeriod: str | None = None
    LatePeriod: str | None = None


class GenusRead(GenusBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class GenusDetail(GenusDetailBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
