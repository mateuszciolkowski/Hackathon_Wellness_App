from pydantic import BaseModel, Field
from datetime import date
from .base import BaseSchema

class DayBase(BaseModel):
    diary_id: int
    main_entry: str
    day_rating: int | None = Field(None, ge=0, le=100)  # Dodajemy walidację zakresu

class DayCreate(DayBase):
    pass

class DayResponse(DayBase, BaseSchema):
    id: int
    created_at: date