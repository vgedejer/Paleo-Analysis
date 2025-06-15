from pydantic import BaseModel, EmailStr

# User Base Schema - shared properties for reading and writing
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    favorite_dino: str | None = None

# User Create Schema - properties for creating a user
class UserCreate(UserBase):
    pass

# User Output Schema - properties for reading a user from the database
class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True