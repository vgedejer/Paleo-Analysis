from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database.db_connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    favorite_dino = Column(String, index=True)

    created_at = Column(DateTime, index=True)
    last_modified = Column(DateTime, index=True)
