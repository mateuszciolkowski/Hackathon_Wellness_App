from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import User
from ..schemas.user import UserCreate, UserResponse, UserLogin, UserLoginResponse
from ..dependencies import get_db
from app.crud import users
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Sprawdź, czy użytkownik o takim emailu już istnieje
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email już zarejestrowany")
    # Użyj funkcji create_user z crud/users.py
    return users.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")
    return user

@router.get("/by-email/{email}", response_model=UserResponse)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")
    return user

# Konfiguracja JWT
SECRET_KEY = "twój_tajny_klucz"  # Należy przenieść do zmiennych środowiskowych
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=UserLoginResponse)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")
    
    if not pwd_context.verify(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Nieprawidłowe hasło")
    
    # Generowanie tokenu JWT
    access_token = create_access_token(
        data={"sub": user.email}
    )
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "access_token": access_token,
        "token_type": "bearer"
    }


#do tworzenia wpisu potrzeba
#akltualna data wpisu 
#tresc
#userid / username
#
#jak wyslemy do bazy to returnujemy potweirdzenie
