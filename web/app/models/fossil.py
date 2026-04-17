from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base


class Fossil(Base):
    __tablename__ = "dino_fossils"

    id = Column("index", Integer, primary_key=True, index=True)
    Fossil = Column(String, index=True)
    Longitude = Column(Float, index=True)
    Latitude = Column(Float, index=True)
    Formation = Column(String, index=True)
    Country = Column(String, index=True)
    State = Column(String, index=True)
    County = Column(String, index=True)
    Collection = Column(Integer, index=True)
    GeoComments = Column(String, index=True)
    PaleoLongitude = Column(Float, index=True)
    PaleoLatitude = Column(Float, index=True)
    GeoPlate = Column(String, index=True)
    GeoGroup = Column(String, index=True)
    Member = Column(String, index=True)
    PaleoModel = Column(String, index=True)

    genus_id = Column(Integer, ForeignKey("dino_genera.index"), index=True)
    genus = relationship("Genus", back_populates="fossils")
