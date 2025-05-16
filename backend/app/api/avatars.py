from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/avatars", tags=["avatars"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{diary_id}", response_model=schemas.Avatar)
def create_avatar(diary_id: int, db: Session = Depends(get_db)):
    db_avatar = crud.avatars.get_avatar_by_diary_id(db, diary_id=diary_id)
    if db_avatar:
        raise HTTPException(status_code=400, detail="Avatar for diary already exists")
    return crud.avatars.create_avatar(db=db, diary_id=diary_id)

@router.get("/{avatar_id}", response_model=schemas.Avatar)
def read_avatar(avatar_id: int, db: Session = Depends(get_db)):
    db_avatar = crud.avatars.get_avatar(db, avatar_id=avatar_id)
    if not db_avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    return db_avatar