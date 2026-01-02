from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db_connection import Base

class DinoFossil(Base):
    __tablename__ = "dino_fossils"

    index = Column(Integer, primary_key=True, index=True)
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

    genus_id = Column(Integer, ForeignKey('dino_genus.index'), index=True)
    genus = relationship("DinoGenus", back_populates="fossils")
