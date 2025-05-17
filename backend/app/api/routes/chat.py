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
        
        # Wczytaj prompt psychologiczny
        with open('/Users/mciolkowski/Desktop/HACK/backend/prompts/ai_psycho.txt', 'r') as file:
            psycho_prompt = file.read()
        
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
        
        # Wczytaj prompt z pliku
        with open('/Users/mciolkowski/Desktop/HACK/backend/prompts/questions.txt', 'r') as file:
            prompt_template = file.read()
        
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
        qa = db.query(QuestionAnswer).filter(  # Zmieniamy QuestionsAnswers na QuestionAnswer
            QuestionAnswer.day_id == request.day_id
        ).all()
        
        if not qa:
            raise HTTPException(status_code=404, detail="Nie znaleziono pytań dla tego dnia")
        
        # Przygotuj prompt dla OpenAI
        prompt = "Przesle ci zaraz pytania oraz odpowiedzi na ktore uzytkownik odpowiedzial chcialbym bys je przeanalizowal i ocenil w skali 1/100 jakie samopoczucie towarzyszy osobie ktora na nie odpowiedzial odpowiedz jedna liczba. Nie chce bys odpisywal jakiekolwiek inne slowo ani emotke niz liczba\n\n"
        
        for item in qa:
            prompt += f"Pytanie: {item.question}\nOdpowiedź: {item.answer}\n\n"
        
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