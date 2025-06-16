from database.db_connection import Base, engine
from models import user

Base.metadata.create_all(bind=engine)