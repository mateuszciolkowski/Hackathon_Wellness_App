import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from ..schemas.question_answer import QuestionAnswerCreate, QuestionAnswerResponse, QuestionsAnswersCreate
from ..models.question_answer import QuestionAnswer
from ..dependencies import get_db
from app.models import Day
from .chat import ChatResponse

# Konfiguracja loggera
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/batch", response_model=List[QuestionAnswerResponse])
def create_questions_answers(qa_data: QuestionsAnswersCreate, db: Session = Depends(get_db)):
    logger.info(f"Próba utworzenia zestawu pytań i odpowiedzi dla dnia {qa_data.day_id}")
    
    # Sprawdź czy dzień istnieje
    day = db.query(Day).filter(Day.id == qa_data.day_id).first()
    if not day:
        logger.warning(f"Dzień o ID {qa_data.day_id} nie został znaleziony")
        raise HTTPException(status_code=404, detail="Dzień nie znaleziony")

    created_qas = []
    try:
        for qa in qa_data.questions_answers:
            db_qa = QuestionAnswer(
                day_id=qa_data.day_id,
                question=qa.question,
                answer=qa.answer
            )
            db.add(db_qa)
            created_qas.append(db_qa)
        
        db.commit()
        for qa in created_qas:
            db.refresh(qa)
        
        logger.info(f"Pomyślnie utworzono {len(created_qas)} pytań i odpowiedzi")
        return created_qas
    except Exception as e:
        db.rollback()
        logger.error(f"Błąd podczas dodawania pytań i odpowiedzi: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Błąd podczas tworzenia pytań i odpowiedzi: {str(e)}")

@router.get("/day/{day_id}", response_model=List[QuestionAnswerResponse])
def get_questions_answers_by_day(day_id: int, db: Session = Depends(get_db)):
    logger.info(f"Pobieranie pytań i odpowiedzi dla dnia {day_id}")
    
    qas = db.query(QuestionAnswer).filter(QuestionAnswer.day_id == day_id).all()
    if not qas:
        logger.warning(f"Nie znaleziono pytań i odpowiedzi dla dnia {day_id}")
        raise HTTPException(status_code=404, detail="Nie znaleziono pytań i odpowiedzi dla tego dnia")
    
    return qas


class DayQuestionsResponse(BaseModel):
    day_id: int
    created_at: date
    day_rating: int
    main_entry: Optional[str]
    questions: List[QuestionAnswerResponse]

@router.get("/history/{diary_id}", response_model=List[DayQuestionsResponse])
def get_questions_history(diary_id: int, db: Session = Depends(get_db)):
    """
    Pobiera historię pytań i odpowiedzi dla określonego dziennika, pogrupowaną po dniach.
    """
    logger.info(f"Pobieranie historii pytań i odpowiedzi dla dziennika: {diary_id}")
    
    try:
        # Znajdź wszystkie dni dla danego dziennika
        days = db.query(Day).filter(Day.diary_id == diary_id).all()
        if not days:
            logger.warning(f"Nie znaleziono dni dla dziennika {diary_id}")
            raise HTTPException(
                status_code=404,
                detail="Nie znaleziono dni dla tego dziennika"
            )
        
        # Przygotuj odpowiedź pogrupowaną po dniach
        grouped_response = []
        for day in days:
            # Pobierz pytania dla danego dnia
            questions = db.query(QuestionAnswer)\
                .filter(QuestionAnswer.day_id == day.id)\
                .order_by(QuestionAnswer.id)\
                .all()
                
            if questions:
                grouped_response.append({
                    "day_id": day.id,
                    "created_at": day.created_at,
                    "day_rating": day.day_rating,
                    "main_entry": day.main_entry,
                    "questions": questions
                })
        
        if not grouped_response:
            logger.warning(f"Nie znaleziono pytań dla dziennika {diary_id}")
            raise HTTPException(
                status_code=404,
                detail="Nie znaleziono pytań dla tego dziennika"
            )
        
        # Zmieniono sortowanie na rosnące (od najstarszego do najnowszego)
        grouped_response.sort(key=lambda x: x["created_at"])  # Usunięto reverse=True
        
        logger.info(f"Znaleziono pytania dla {len(grouped_response)} dni w dzienniku {diary_id}")
        return grouped_response
        
    except Exception as e:
        logger.error(f"Błąd podczas pobierania historii pytań: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas pobierania historii pytań: {str(e)}"
        )


@router.post("/psycho-analysis/{diary_id}", response_model=ChatResponse)
def psycho_analysis(diary_id: int, db: Session = Depends(get_db)):
    """
    Analizuje historię pytań i odpowiedzi dla dziennika z perspektywy psychologicznej.
    """
    try:
        # Pobierz historię pytań
        days_data = get_questions_history(diary_id, db)
        
        # Zdefiniuj prompt psychoanalityczny bezpośrednio w kodzie
        psycho_prompt = """Dostajesz dane ktore mowia o tym masz nastoj przez ostatnie dni chce bys dokladnie to przeanalizowal wzgledem twojego zdrowia posychicznego i napisal co mozemy z tym zrobic zeby poczuc sie lepiej. Napisz zwiezle i na temat"""
        
        # Przygotuj dane do analizy
        analysis_data = psycho_prompt + "\n\nDane do analizy:\n"
        for day in days_data:
            analysis_data += f"Data: {day['created_at']}, Ocena dnia: {day['day_rating']}\n"
            for qa in day['questions']:
                analysis_data += f"Pytanie: {qa.question}\nOdpowiedź: {qa.answer}\n\n"
        
        # Dodaj import klienta OpenAI
        import openai
        import os
        from dotenv import load_dotenv
        load_dotenv()
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Wyślij do OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś analitykiem psychologicznym."},
                {"role": "user", "content": analysis_data}
            ]
        )
        
        return ChatResponse(response=completion.choices[0].message.content)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas analizy psychologicznej: {str(e)}"
        )