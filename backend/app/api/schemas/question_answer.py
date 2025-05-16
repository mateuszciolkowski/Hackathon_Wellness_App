from pydantic import BaseModel
from typing import Optional, List

class QuestionAnswerBase(BaseModel):
    question: str
    answer: Optional[str] = None
    day_id: int

class QuestionAnswerCreate(QuestionAnswerBase):
    pass

class QuestionAnswerResponse(QuestionAnswerBase):
    id: int

    class Config:
        from_attributes = True

class QuestionsAnswersCreate(BaseModel):
    day_id: int
    questions_answers: List[QuestionAnswerCreate]