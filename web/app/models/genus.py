from sqlalchemy import Boolean, Column, Float, Integer, String, text
from sqlalchemy.orm import relationship
from db.base import Base


class Genus(Base):
    __tablename__ = "genera"

    id = Column(Integer, primary_key=True)
    # Taxonomic group this row belongs to (e.g. "Dinosauria", "Mammalia").
    # Lets every clade share one set of tables, so adding a new group is a data
    # load (one more ingestion run) rather than new tables + endpoints.
    clade = Column(String, nullable=False, index=True, server_default=text("'Dinosauria'"))
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
