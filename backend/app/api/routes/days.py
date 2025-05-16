from typing import List
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import date
# from ..schemas.day import DayCreate, DayResponse
# from ..models.day import Day
# from ..dependencies import get_db
# from app.models import User, Diary

# router = APIRouter()

# @router.post("/", response_model=DayResponse)
# def create_day_entry(day_data: DayCreate, db: Session = Depends(get_db)):
#     # Sprawdź, czy dziennik istnieje
#     diary = db.query(Diary).filter(Diary.id == day_data.diary_id).first()
#     if not diary:
#         raise HTTPException(status_code=404, detail="Dziennik nie znaleziony")
    
#     # Utwórz nowy wpis - nie musimy podawać created_at, baza doda go automatycznie
#     db_day = Day(
#         diary_id=day_data.diary_id,
#         main_entry=day_data.main_entry,
#         day_rating=day_data.day_rating
#     )
    
#     try:
#         db.add(db_day)
#         db.commit()
#         db.refresh(db_day)
#         return db_day
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Błąd podczas tworzenia wpisu: {str(e)}")

# @router.get("/{day_id}", response_model=DayResponse)
# def read_day(day_id: int, db: Session = Depends(get_db)):
#     day = db.query(Day).filter(Day.id == day_id).first()
#     if day is None:
#         raise HTTPException(status_code=404, detail="Dzień nie znaleziony")
#     return day

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from ..schemas.day import DayCreate, DayResponse
from ..models.day import Day
from ..dependencies import get_db
from app.models import User, Diary

# Konfiguracja loggera
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/", response_model=DayResponse)
def create_day_entry(day_data: DayCreate, db: Session = Depends(get_db)):
    logger.info(f"Próba utworzenia wpisu dnia: {day_data}")
    
    diary = db.query(Diary).filter(Diary.id == day_data.diary_id).first()
    if not diary:
        logger.warning(f"Dziennik o ID {day_data.diary_id} nie został znaleziony.")
        raise HTTPException(status_code=404, detail="Dziennik nie znaleziony")
    
    db_day = Day(
        diary_id=day_data.diary_id,
        main_entry=day_data.main_entry,
        day_rating=day_data.day_rating
    )
    
    try:
        db.add(db_day)
        db.commit()
        db.refresh(db_day)
        logger.info(f"Utworzono wpis dnia: {db_day}")
        return db_day
    except Exception as e:
        db.rollback()
        logger.error(f"Błąd podczas dodawania wpisu do bazy danych: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Błąd podczas tworzenia wpisu: {str(e)}")

@router.get("/{day_id}", response_model=DayResponse)
def read_day(day_id: int, db: Session = Depends(get_db)):
    logger.info(f"Żądanie odczytu wpisu dnia o ID: {day_id}")
    day = db.query(Day).filter(Day.id == day_id).first()
    if day is None:
        logger.warning(f"Wpis dnia o ID {day_id} nie został znaleziony.")
        raise HTTPException(status_code=404, detail="Dzień nie znaleziony")
    
    logger.info(f"Znaleziono wpis dnia: {day}")
    return day

@router.get("/by-date/{date}", response_model=List[DayResponse])
def read_days_by_date(date: date, db: Session = Depends(get_db)):
    logger.info(f"Żądanie odczytu wpisów z dnia: {date}")
    
    days = db.query(Day).filter(Day.created_at == date).all()
    if not days:
        logger.warning(f"Nie znaleziono wpisów z dnia {date}")
        raise HTTPException(status_code=404, detail="Nie znaleziono wpisów dla podanej daty")
    
    logger.info(f"Znaleziono {len(days)} wpisów z dnia {date}")
    return days
