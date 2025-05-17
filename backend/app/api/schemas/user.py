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


class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    id: int
    email: str
    name: str
    access_token: str
    token_type: str