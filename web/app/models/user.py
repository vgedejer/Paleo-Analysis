from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database.db_connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    favorite_dino = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    middle_initial = Column(String, index=True, nullable=True)

    created_on = Column(DateTime, index=True)
    last_modified = Column(DateTime, index=True)
