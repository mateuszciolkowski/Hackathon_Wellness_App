from sqlalchemy.orm import Session
from app import models, schemas

def get_avatar(db: Session, avatar_id: int):
    return db.query(models.Avatar).filter(models.Avatar.id == avatar_id).first()

def get_avatar_by_diary_id(db: Session, diary_id: int):
    return db.query(models.Avatar).filter(models.Avatar.diary_id == diary_id).first()

def create_avatar(db: Session, diary_id: int):
    db_avatar = models.Avatar(diary_id=diary_id)
    db.add(db_avatar)
    db.commit()
    db.refresh(db_avatar)
    return db_avatar