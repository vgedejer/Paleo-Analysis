from sqlalchemy.orm import Session
from models.user import User
from schema.user import UserCreate
from datetime import datetime, timezone

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=str(user.email),
        favorite_dinos=user.favorite_dinos,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_initial=user.middle_initial,

        created_on= datetime.now(timezone.utc),
        last_modified=datetime.now(timezone.utc),
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

def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    return user

