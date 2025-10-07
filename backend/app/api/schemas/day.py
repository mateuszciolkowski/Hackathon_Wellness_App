from pydantic import BaseModel, Field
from datetime import date
from .base import BaseSchema
from typing import Optional

class DayBase(BaseModel):
    diary_id: int
    main_entry: str
    # day_rating: int | None = Field(None, ge=0, le=100)  # Dodajemy walidację zakresu
    day_rating: Optional[int] = Field(None, ge=0, le=100)
    
class DayCreate(BaseModel):
    user_id: int
    main_entry: str
    day_rating: Optional[int] = None

class DayResponse(DayBase, BaseSchema):
    id: int
    created_at: date