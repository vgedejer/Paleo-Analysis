from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate


def list_all(db: Session) -> list[User]:
    return db.query(User).all()


def get_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def create(db: Session, payload: UserCreate) -> User:
    now = datetime.now(timezone.utc)
    user = User(
        username=payload.username,
        email=str(payload.email),
        favorite_dino=payload.favorite_dino,
        first_name=payload.first_name,
        last_name=payload.last_name,
        middle_initial=payload.middle_initial,
        created_on=now,
        last_modified=now,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
