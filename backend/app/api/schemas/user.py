from pydantic import BaseModel, EmailStr
from .base import BaseSchema

class UserBase(BaseModel):
    name: str
    nickname: str
    email: str
    birth_year: int
    

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase, BaseSchema):
    id: int