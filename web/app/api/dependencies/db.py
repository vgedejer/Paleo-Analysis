from database.db_connection import SessionLocal

def get_db():

    print("getting database session..")
    db = SessionLocal()
    try:
        yield db
    finally:
        print("closing database..")
        db.close()
