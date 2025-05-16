from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models.diary import Diary
from ..schemas.diary import DiaryCreate, DiaryResponse
from ..dependencies import get_db

router = APIRouter()

@router.post("/", response_model=DiaryResponse)
def create_diary(diary: DiaryCreate, db: Session = Depends(get_db)):
    db_diary = Diary(**diary.dict())
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    return db_diary

@router.get("/{diary_id}", response_model=DiaryResponse)
def read_diary(diary_id: int, db: Session = Depends(get_db)):
    diary = db.query(Diary).filter(Diary.id == diary_id).first()
    if diary is None:
        raise HTTPException(status_code=404, detail="Dziennik nie znaleziony")
    return diary