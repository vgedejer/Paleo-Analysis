from sqlalchemy import Column, Integer, String, Float, Boolean
from database.db_connection import Base

class DinoSpecies(Base):
    __tablename__ = "dino_species"

    index = Column(Integer, primary_key=True, index=True)
    Species = Column(String, index=True)
    Genus = Column(String, index=True)
    Diet = Column(String, index=True)
    MaxMYA = Column(Integer, index=True)
    MinMYA = Column(Integer, index=True)
    LifespanMYA = Column(Float, index=True)
    EarlyAge = Column(String, index=True)
    LateAge = Column(String, index=True)
    EarlyPeriod = Column(String, index=True)
    LatePeriod = Column(String, index=True)
