from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base


class Genus(Base):
    __tablename__ = "dino_genera"

    id = Column("index", Integer, primary_key=True, index=True)
    Genus = Column(String, index=True)
    Family = Column(String, index=True)
    Infraorder = Column(String, index=True)
    Suborder = Column(String, index=True)
    Order = Column(String, index=True)
    Informal = Column(Boolean, index=True)
    TaxonSize = Column(Integer, index=False)
    Diet = Column(String, index=True)
    MaxMYA = Column(Float, index=True)
    MinMYA = Column(Float, index=True)
    LifespanMYA = Column(Float, index=True)
    EarlyAge = Column(String, index=True)
    LateAge = Column(String, index=True)
    EarlyPeriod = Column(String, index=True)
    LatePeriod = Column(String, index=True)

    fossils = relationship("Fossil", back_populates="genus")
    species = relationship("Species", back_populates="genus")
