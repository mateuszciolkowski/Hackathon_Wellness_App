from sqlalchemy.orm import Session
from app import models, schemas
from datetime import date

def get_day(db: Session, day_id: int):
    return db.query(models.Day).filter(models.Day.id == day_id).first()

def create_day(db: Session, day: schemas.DayCreate, diary_id: int):
    db_day = models.Day(
        diary_id=diary_id,
        main_entry=day.main_entry,
        created_at=day.created_at or date.today()
    )
    db.add(db_day)
    db.commit()
    db.refresh(db_day)

    # opcjonalnie dodaj pytania i odpowiedzi
    for qa in day.questions_answers:
        from app.models import QuestionAnswer
        db_qa = QuestionAnswer(day_id=db_day.id, question=qa.question, answer=qa.answer)
        db.add(db_qa)
    db.commit()
    return db_day