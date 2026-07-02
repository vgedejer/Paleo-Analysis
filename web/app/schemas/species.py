from __future__ import annotations
from pydantic import BaseModel, ConfigDict


class SpeciesBase(BaseModel):
    Species: str
    Genus: str
    Diet: str
    EarlyPeriod: str
    LatePeriod: str


class SpeciesCreate(SpeciesBase):
    pass


class SpeciesUpdate(BaseModel):
    Species: str | None = None
    Genus: str | None = None
    Diet: str | None = None
    MaxMYA: float | None = None
    MinMYA: float | None = None
    LifespanMYA: float | None = None
    EarlyAge: str | None = None
    LateAge: str | None = None
    EarlyPeriod: str | None = None
    LatePeriod: str | None = None


class SpeciesRead(SpeciesBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
