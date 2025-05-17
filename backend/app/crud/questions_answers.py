from sqlalchemy.orm import Session
from app import models, schemas

def get_question_answer(db: Session, qa_id: int):
    return db.query(models.QuestionAnswer).filter(models.QuestionAnswer.id == qa_id).first()

def create_question_answer(db: Session, qa: schemas.QuestionAnswerCreate, day_id: int):
    db_qa = models.QuestionAnswer(day_id=day_id, question=qa.question, answer=qa.answer)
    db.add(db_qa)
    db.commit()
    db.refresh(db_qa)
    return db_qa