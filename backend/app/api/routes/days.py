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
    
    # Znajdź dziennik użytkownika
    diary = db.query(Diary).filter(Diary.user_id == day_data.user_id).first()
    if not diary:
        logger.warning(f"Nie znaleziono dziennika dla użytkownika o ID {day_data.user_id}")
        raise HTTPException(status_code=404, detail="Nie znaleziono dziennika dla tego użytkownika")
    
    # Utwórz nowy wpis
    db_day = Day(
        diary_id=diary.id,  # Używamy ID znalezionego dziennika
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

#endpoint dla zapytania o wszystkie dni z pamietnika z danego użytkownika - frontend przekazuje iduzytkownika
@router.get("/by-user/{user_id}", response_model=List[DayResponse])
def read_days_by_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Żądanie odczytu wpisów dla użytkownika o ID: {user_id}")

    # Pobierz wszystkie diaries użytkownika
    diaries = db.query(Diary).filter(Diary.user_id == user_id).all()

    # Pobierz wszystkie dni dla każdego diarie
    days = []
    for diary in diaries:
        days.extend(db.query(Day).filter(Day.diary_id == diary.id).all())

    if not days:
        logger.warning(f"Nie znaleziono wpisów dla użytkownika o ID {user_id}")
        raise HTTPException(status_code=404, detail="Nie znaleziono wpisów dla podanego użytkownika")

    logger.info(f"Znaleziono {len(days)} wpisów dla użytkownika o ID {user_id}")
    return days

@router.get("/", response_model=List[DayResponse])
def read_all_days(db: Session = Depends(get_db)):
    days = db.query(Day).all()
    return days

@router.get("/by-diary/{diary_id}", response_model=List[DayResponse])
def read_days_by_diary(diary_id: int, db: Session = Depends(get_db)):
    days = db.query(Day).filter(Day.diary_id == diary_id).all()
    if not days:
        raise HTTPException(status_code=404, detail="Nie znaleziono dni dla tego dziennika")
    return days


@router.put("/{day_put_id}", response_model=DayResponse)
def update_day_entry(day_id: int, day_data: DayCreate, db: Session = Depends(get_db)):
    logger.info(f"Próba aktualizacji wpisu dnia o ID {day_id}: {day_data}")
    
    # Znajdź istniejący wpis
    db_day = db.query(Day).filter(Day.id == day_id).first()
    if not db_day:
        logger.warning(f"Nie znaleziono wpisu dnia o ID {day_id}")
        raise HTTPException(status_code=404, detail="Nie znaleziono wpisu dnia")
    
    # Aktualizuj pola
    db_day.main_entry = day_data.main_entry
    db_day.day_rating = day_data.day_rating
    
    try:
        db.commit()
        db.refresh(db_day)
        logger.info(f"Zaktualizowano wpis dnia: {db_day}")
        return db_day
    except Exception as e:
        db.rollback()
        logger.error(f"Błąd podczas aktualizacji wpisu: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Błąd podczas aktualizacji wpisu: {str(e)}")
