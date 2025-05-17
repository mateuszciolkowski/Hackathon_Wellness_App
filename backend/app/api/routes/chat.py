from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import time
from app.api.dependencies import get_db
from app.models import Day, Diary, QuestionAnswer
from app.api.models.conversation import Conversation, Message  # Dodajemy brakujące importy
import json

# Załaduj zmienne środowiskowe
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

class ChatMessage(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str  # Zmieniamy z powrotem na str, bo OpenAI zwraca string JSON

@router.post("/send", response_model=ChatResponse)
async def send_message(message: ChatMessage, db: Session = Depends(get_db)):
    try:
        time.sleep(1)
        
        # Pobierz ostatnią konwersację lub utwórz nową
        conversation = db.query(Conversation).order_by(Conversation.id.desc()).first()
        if not conversation:
            conversation = Conversation(user_id=1)
            db.add(conversation)
            db.commit()
        
        # Pobierz historię konwersacji
        history = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at).all()
        
        # Wczytaj prompt psychologiczny - zamiana na statyczny prompt
        psycho_prompt = """Jestem osoba ktora zawsze chetnie z tobą porozmawia. Pomogę ci przeanalizować twoje samopoczucie i emocje. Będę odpowiadał w sposób empatyczny i wspierający, zawsze z troską o twoje dobro. Skupię się na twoich uczuciach i pomogę ci lepiej je zrozumieć."""
        
        # Przygotuj kontekst dla OpenAI
        messages = [
            {"role": "system", "content": psycho_prompt}
        ]
        
        # Dodaj historię rozmów jeśli istnieje
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Dodaj nową wiadomość użytkownika
        messages.append({"role": "user", "content": message.prompt})
        
        # Wyślij do OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        # Zapisz odpowiedź asystenta
        ai_response = completion.choices[0].message.content
        assistant_msg = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response
        )
        db.add(assistant_msg)
        db.commit()
        
        return ChatResponse(response=ai_response)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas komunikacji z OpenAI: {str(e)}"
        )

class BlogPostQuestionRequest(BaseModel):
    user_id: int

@router.post("/generate-questions", response_model=ChatResponse)
async def generate_questions(request: BlogPostQuestionRequest, db: Session = Depends(get_db)):
    try:
        # Pobierz ostatni wpis z największym ID
        last_entry = db.query(Day).order_by(Day.id.desc()).first()
        if not last_entry:
            raise HTTPException(status_code=404, detail="Nie znaleziono żadnych wpisów")
        
        # Statyczny prompt zamiast wczytywania z pliku
        prompt_template = """Wygeneruj 3 pytania dotyczące wpisu użytkownika. Pytania powinny pomóc w głębszej analizie emocji i samopoczucia. Odpowiedź zwróć w formacie JSON z tablicą pytań. Na przykład:
{
    "questions": [
        "Jak się czułeś w tym momencie?",
        "Co najbardziej wpłynęło na twoje emocje?",
        "Jakie wnioski wyciągasz z tej sytuacji?"
    ]
}"""
        
        # Połącz prompt z treścią wpisu
        full_prompt = f"{prompt_template}\n\nTreść wpisu:\n{last_entry.main_entry}"
        
        # Wyślij do OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś pomocnym asystentem."},
                {"role": "user", "content": full_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return ChatResponse(response=json.dumps(completion.choices[0].message.content))
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas generowania pytań: {str(e)}"
        )


class AnalyzeAnswersRequest(BaseModel):
    day_id: int

@router.post("/analyze-mood", response_model=ChatResponse)
async def analyze_mood(request: AnalyzeAnswersRequest, db: Session = Depends(get_db)):
    try:
        # Pobierz pytania i odpowiedzi dla danego dnia
        qa = db.query(QuestionAnswer).filter(
            QuestionAnswer.day_id == request.day_id
        ).all()
        
        if not qa:
            raise HTTPException(status_code=404, detail="Nie znaleziono pytań dla tego dnia")
        
        # Statyczny prompt zamiast przygotowywania dynamicznego
        prompt = """Przeanalizuj odpowiedzi użytkownika i oceń jego samopoczucie w skali 1-100. Odpowiedz tylko liczbą, bez dodatkowego tekstu czy emotikon. Wyższa liczba oznacza lepsze samopoczucie."""
        
        for item in qa:
            prompt += f"\nPytanie: {item.question}\nOdpowiedź: {item.answer}\n"
        
        # Wyślij do OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś analitykiem nastroju. Zwracasz tylko liczby."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parsuj odpowiedź i zaktualizuj day_rating
        rating = int(completion.choices[0].message.content)
        day = db.query(Day).filter(Day.id == request.day_id).first()
        day.day_rating = rating
        db.commit()
        
        return ChatResponse(response=str(rating))
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas analizy nastroju: {str(e)}"
        )


class DailyAdviceRequest(BaseModel):
    user_id: int

@router.get("/daily-advice", response_model=ChatResponse)
async def get_daily_advice(db: Session = Depends(get_db)):
    try:
        # Statyczny prompt dla generowania codziennej rady
        prompt = """Wygeneruj krótką, jedną zdaniową radę dotyczącą zdrowia psychicznego na dzisiaj. 
        Rada powinna być pozytywna, praktyczna i motywująca. Odpowiedz tylko jednym zdaniem."""
        
        # Wyślij do OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś psychologiem specjalizującym się w zdrowiu psychicznym."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return ChatResponse(response=completion.choices[0].message.content)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas generowania codziennej rady: {str(e)}"
        )

@router.post("/send", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    try:
        # Statyczny prompt psychologiczny
        psycho_prompt = """Jestem twoim osobistym asystentem psychologicznym. Pomogę ci przeanalizować twoje samopoczucie i emocje. Będę odpowiadał w sposób empatyczny i wspierający, zawsze z troską o twoje dobro. Skupię się na twoich uczuciach i pomogę ci lepiej je zrozumieć."""
        
        # Przygotuj kontekst dla OpenAI
        messages = [
            {"role": "system", "content": psycho_prompt},
            {"role": "user", "content": message.prompt}
        ]
        
        # Wyślij do OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        # Pobierz odpowiedź AI
        ai_response = completion.choices[0].message.content
        
        return ChatResponse(response=ai_response)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas komunikacji z OpenAI: {str(e)}"
        )