from sqlalchemy.orm import Session
from models.user import User
from schema.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=str(user.email),
        full_name=user.full_name,
        favorite_dino=user.favorite_dino
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def remove_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False