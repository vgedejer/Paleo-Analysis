from pydantic import BaseModel, EmailStr
from datetime import datetime

# User Base Schema - shared properties for reading and writing
class UserBase(BaseModel):
    username: str
    email: EmailStr
    favorite_dino: str | None = None

# User Create Schema - properties for creating a user
class UserCreate(UserBase):
    first_name: str
    last_name: str
    middle_initial: str | None = None
    pass

# User Output Schema - properties for reading a user from the database
class UserOut(UserBase):
    full_name: str | None = None
    id: int

    class Config:
        orm_mode = True