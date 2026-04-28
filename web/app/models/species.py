from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base


class Species(Base):
    __tablename__ = "dino_species"

    id = Column("index", Integer, primary_key=True, index=True)
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

    genus_id = Column(Integer, ForeignKey("dino_genera.index"), index=True)
    genus = relationship("Genus", back_populates="species")
