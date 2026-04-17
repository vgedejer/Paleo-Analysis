"""Users router — RESTful conventions.

- GET    /users                 (list, optional ?username= filter)
- POST   /users                 -> 201
- GET    /users/{id}
- DELETE /users/{id}            -> 204
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.user import UserCreate, UserRead
from services import user_service

router = APIRouter()


@router.get("", response_model=list[UserRead])
def list_users(
    username: str | None = None,
    db: Session = Depends(get_db),
) -> list[UserRead]:
    if username is not None:
        return [user_service.get_user_by_username(db, username)]
    return user_service.list_users(db)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    return user_service.create_user(db, payload)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserRead:
    return user_service.get_user_by_id(db, user_id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> Response:
    user_service.delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
