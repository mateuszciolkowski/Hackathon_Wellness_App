from pydantic import BaseModel
from datetime import date
from .base import BaseSchema

class DayBase(BaseModel):
    diary_id: int
    main_entry: str | None = None

class DayCreate(DayBase):
    pass

class DayResponse(DayBase, BaseSchema):
    id: int
    created_at: date