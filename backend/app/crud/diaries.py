from sqlalchemy.orm import Session
from app import models, schemas

def get_diary(db: Session, diary_id: int):
    return db.query(models.Diary).filter(models.Diary.id == diary_id).first()

def get_diary_by_user_id(db: Session, user_id: int):
    return db.query(models.Diary).filter(models.Diary.user_id == user_id).first()

def create_diary(db: Session, diary: schemas.DiaryCreate):
    db_diary = models.Diary(user_id=diary.user_id)
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    return db_diary