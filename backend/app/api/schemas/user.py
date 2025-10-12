from pydantic import BaseModel, EmailStr, validator
from .base import BaseSchema

class UserBase(BaseModel):
    name: str
    nickname: str
    email: str
    birth_year: int


class UserCreate(UserBase):
    password: str
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Nazwa nie może być pusta')
        return v.strip()
    
    @validator('nickname')
    def nickname_must_not_be_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Nickname nie może być pusty')
        return v.strip()
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if not v or '@' not in v or '.' not in v:
            raise ValueError('Nieprawidłowy format emaila')
        return v.strip().lower()
    
    @validator('password')
    def password_must_be_strong(cls, v):
        if not v or len(v) < 6:
            raise ValueError('Hasło musi mieć co najmniej 6 znaków')
        return v
    
    @validator('birth_year')
    def birth_year_must_be_valid(cls, v):
        from datetime import datetime
        current_year = datetime.now().year
        if v < 1900 or v > current_year:
            raise ValueError('Nieprawidłowy rok urodzenia')
        return v

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