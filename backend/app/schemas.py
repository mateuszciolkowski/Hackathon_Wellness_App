from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import date

class QuestionAnswerBase(BaseModel):
    question: str
    answer: Optional[str] = None

class QuestionAnswerCreate(QuestionAnswerBase):
    pass

class QuestionAnswer(QuestionAnswerBase):
    id: int
    day_id: int

    class Config:
        orm_mode = True

class DayBase(BaseModel):
    main_entry: Optional[str] = None
    created_at: Optional[date]

class DayCreate(DayBase):
    questions_answers: List[QuestionAnswerCreate] = []

class Day(DayBase):
    id: int
    diary_id: int
    questions_answers: List[QuestionAnswer] = []

    class Config:
        orm_mode = True

class AvatarBase(BaseModel):
    pass  # możesz dodać np. url avatara

class AvatarCreate(AvatarBase):
    pass

class Avatar(AvatarBase):
    id: int
    diary_id: int

    class Config:
        orm_mode = True

class DiaryBase(BaseModel):
    user_id: int

class DiaryCreate(DiaryBase):
    pass

class Diary(DiaryBase):
    id: int
    days: List[Day] = []
    avatar: Optional[Avatar]

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    nickname: str
    email: EmailStr
    birth_year: int

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    diary: Optional[Diary]

    class Config:
        orm_mode = True