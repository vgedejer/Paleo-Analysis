from sqlalchemy import Column, Integer, String, Float, Boolean
from database.db_connection import Base

class DinoGenus(Base):
    __tablename__ = "dino_genera"

    index = Column(Integer, primary_key=True, index=True)
    Genus = Column(String, index=True)
    Family = Column(String, index=True)
    Infraorder = Column(String, index=True)
    Suborder = Column(String, index=True)
    Order = Column(String, index=True)
    Informal = Column(Integer, index=True)
    TaxonSize = Column(String, index=False)
    Diet = Column(String, index=True)
    MaxMYA = Column(Integer, index=True)
    MinMYA = Column(Integer, index=True)
    LifespanMYA = Column(Float, index=True)
    EarlyAge = Column(String, index=True)
    LateAge = Column(String, index=True)
    EarlyPeriod = Column(String, index=True)
    LatePeriod = Column(String, index=True)
