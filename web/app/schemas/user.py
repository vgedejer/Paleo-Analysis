from __future__ import annotations
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    favorite_dino: str | None = None


class UserCreate(UserBase):
    first_name: str
    last_name: str
    middle_initial: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    favorite_dino: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_initial: str | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str | None = None
