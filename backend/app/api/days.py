from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/days", tags=["days"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{diary_id}", response_model=schemas.Day)
def create_day(diary_id: int, day: schemas.DayCreate, db: Session = Depends(get_db)):
    return crud.days.create_day(db=db, day=day, diary_id=diary_id)

@router.get("/{day_id}", response_model=schemas.Day)
def read_day(day_id: int, db: Session = Depends(get_db)):
    db_day = crud.days.get_day(db, day_id=day_id)
    if not db_day:
        raise HTTPException(status_code=404, detail="Day not found")
    return db_day