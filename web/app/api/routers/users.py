from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schema.user import UserCreate, UserOut
from crud import user as user_crud
from api.dependencies.db import get_db

router = APIRouter()

@router.get("/all")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{user}", response_model=UserOut)
def get_user(user: str, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.username == user).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

@router.post("/create", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db, user)

@router.delete("/delete/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    success = user_crud.remove_user(db, username)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


