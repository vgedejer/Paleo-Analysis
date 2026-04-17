from __future__ import annotations
from sqlalchemy.orm import Session
from core.exceptions import ResourceNotFound
from models.user import User
from repositories import user_repo
from schemas.user import UserCreate, UserRead


def _format_full_name(user: User) -> str:
    parts = f"{user.last_name}, {user.first_name} {user.middle_initial or ''}"
    return parts.strip()


def _to_read(user: User) -> UserRead:
    data = UserRead.model_validate(user)
    data.full_name = _format_full_name(user)
    return data


def list_users(db: Session) -> list[UserRead]:
    return [_to_read(u) for u in user_repo.list_all(db)]


def get_user_by_id(db: Session, user_id: int) -> UserRead:
    user = user_repo.get_by_id(db, user_id)
    if user is None:
        raise ResourceNotFound(f"User with id {user_id} not found")
    return _to_read(user)


def get_user_by_username(db: Session, username: str) -> UserRead:
    user = user_repo.get_by_username(db, username)
    if user is None:
        raise ResourceNotFound(f"User {username!r} not found")
    return _to_read(user)


def create_user(db: Session, payload: UserCreate) -> UserRead:
    user = user_repo.create(db, payload)
    return _to_read(user)


def delete_user(db: Session, user_id: int) -> None:
    user = user_repo.get_by_id(db, user_id)
    if user is None:
        raise ResourceNotFound(f"User with id {user_id} not found")
    user_repo.delete(db, user)
