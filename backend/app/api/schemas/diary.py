from pydantic import BaseModel
from .base import BaseSchema

class DiaryBase(BaseModel):
    user_id: int

class DiaryCreate(DiaryBase):
    pass

class DiaryResponse(DiaryBase, BaseSchema):
    id: int