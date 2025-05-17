from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models import Day, Diary
from datetime import date
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class ChartDataResponse(BaseModel):
    dates: List[date]
    ratings: List[int]

class DateRangeRequest(BaseModel):
    diary_id: int
    start_date: date
    end_date: date

@router.post("/mood-chart/range", response_model=ChartDataResponse)
async def get_mood_chart_data_range(request: DateRangeRequest, db: Session = Depends(get_db)):
    """
    Pobiera dane o nastroju z określonego przedziału czasowego.
    Zwraca dwie listy: daty i odpowiadające im oceny.
    """
    try:
        # Sprawdź czy dziennik istnieje
        diary = db.query(Diary).filter(Diary.id == request.diary_id).first()
        if not diary:
            raise HTTPException(status_code=404, detail="Nie znaleziono dziennika")

        # Pobierz dni z ocenami dla danego dziennika w określonym przedziale czasowym
        days = db.query(Day).filter(
            Day.diary_id == request.diary_id,
            Day.day_rating.isnot(None),
            Day.created_at >= request.start_date,
            Day.created_at <= request.end_date
        ).order_by(Day.created_at).all()

        # Przygotuj oddzielne listy dla dat i ocen
        dates = [day.created_at for day in days]
        ratings = [day.day_rating for day in days]

        return ChartDataResponse(dates=dates, ratings=ratings)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas pobierania danych do wykresu: {str(e)}"
        )