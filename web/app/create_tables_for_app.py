from database.db_connection import Base, engine
from models import user, dino_fossil, dino_genus, dino_species

Base.metadata.create_all(bind=engine)
