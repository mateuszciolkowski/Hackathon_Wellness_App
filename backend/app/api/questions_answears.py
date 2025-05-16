from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/questions_answers", tags=["questions_answers"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{day_id}", response_model=schemas.QuestionAnswer)
def create_qa(day_id: int, qa: schemas.QuestionAnswerCreate, db: Session = Depends(get_db)):
    return crud.questions_answers.create_question_answer(db=db, qa=qa, day_id=day_id)

@router.get("/{qa_id}", response_model=schemas.QuestionAnswer)
def read_qa(qa_id: int, db: Session = Depends(get_db)):
    db_qa = crud.questions_answers.get_question_answer(db, qa_id=qa_id)
    if not db_qa:
        raise HTTPException(status_code=404, detail="QuestionAnswer not found")
    return db_qa