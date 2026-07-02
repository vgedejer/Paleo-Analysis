from sqlalchemy import Column, Float, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from db.base import Base


class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True)
    clade = Column(String, nullable=False, index=True, server_default=text("'Dinosauria'"))
    Species = Column(String, index=True)
    Genus = Column(String, index=True)
    Diet = Column(String, index=True)
    # MYA bounds are fractional (e.g. 66.5); Float keeps them exact under
    # Postgres' strict typing (SQLite tolerated floats in an INTEGER column).
    MaxMYA = Column(Float, index=True)
    MinMYA = Column(Float, index=True)
    LifespanMYA = Column(Float, index=True)
    EarlyAge = Column(String, index=True)
    LateAge = Column(String, index=True)
    EarlyPeriod = Column(String, index=True)
    LatePeriod = Column(String, index=True)

    genus_id = Column(Integer, ForeignKey("genera.id"), index=True)
    genus = relationship("Genus", back_populates="species")
