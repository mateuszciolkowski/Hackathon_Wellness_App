from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..dependencies import get_db
from app.models import Day, Diary
from pydantic import BaseModel

router = APIRouter()

class DayRatingData(BaseModel):
    date: datetime
    rating: int

@router.get("/ratings/user/{user_id}", response_model=List[DayRatingData])
def get_ratings_data(user_id: int, days: int = 30, db: Session = Depends(get_db)):
    """
    Pobiera dane o ocenach dni dla określonego użytkownika.
    :param user_id: ID użytkownika
    :param days: Liczba ostatnich dni do analizy (domyślnie 30)
    :return: Lista dat i ocen
    """
    # Oblicz datę początkową
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Najpierw znajdź dziennik użytkownika
    diary = db.query(Diary).filter(Diary.user_id == user_id).first()
    if not diary:
        raise HTTPException(
            status_code=404,
            detail=f"Nie znaleziono dziennika dla użytkownika {user_id}"
        )
    
    # Pobierz dane z bazy używając diary_id
    ratings = db.query(Day)\
        .filter(Day.diary_id == diary.id)\
        .filter(Day.created_at >= start_date)\
        .filter(Day.created_at <= end_date)\
        .order_by(Day.created_at)\
        .all()
    
    if not ratings:
        raise HTTPException(
            status_code=404,
            detail=f"Nie znaleziono ocen dla użytkownika {user_id} w wybranym okresie"
        )
    
    return [
        DayRatingData(date=rating.created_at, rating=rating.day_rating)
        for rating in ratings
    ]