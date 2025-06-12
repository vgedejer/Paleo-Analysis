from pydantic import BaseModel

class DinoGeneraBase(BaseModel):
    genus: str
    family: str
    infraorder: str
    suborder: str
    order: str
    diet: str
    early_period: str
    late_period: str

class DinoGeneraCreate(DinoGeneraBase):
    pass

class DinoGeneraUpdate(DinoGeneraBase):
    genus: str | None = None
    family: str | None = None
    infraorder: str | None = None
    suborder: str | None = None
    order: str | None = None
    diet: str | None = None
    early_period: str | None = None
    late_period: str | None = None

