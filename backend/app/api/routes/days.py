from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models.day import Day
from ..schemas.day import DayCreate, DayResponse
from ..dependencies import get_db

router = APIRouter()

@router.post("/", response_model=DayResponse)
def create_day(day: DayCreate, db: Session = Depends(get_db)):
    db_day = Day(**day.dict())
    db.add(db_day)
    db.commit()
    db.refresh(db_day)
    return db_day

@router.get("/{day_id}", response_model=DayResponse)
def read_day(day_id: int, db: Session = Depends(get_db)):
    day = db.query(Day).filter(Day.id == day_id).first()
    if day is None:
        raise HTTPException(status_code=404, detail="Dzień nie znaleziony")
    return dayx