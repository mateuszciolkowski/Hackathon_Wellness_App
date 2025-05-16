from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/diaries", tags=["diaries"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Diary)
def create_diary(diary: schemas.DiaryCreate, db: Session = Depends(get_db)):
    return crud.diaries.create_diary(db=db, diary=diary)

@router.get("/{diary_id}", response_model=schemas.Diary)
def read_diary(diary_id: int, db: Session = Depends(get_db)):
    db_diary = crud.diaries.get_diary(db, diary_id=diary_id)
    if not db_diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return db_diary
    