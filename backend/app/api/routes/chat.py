from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import time
from app.api.dependencies import get_db
from app.models import Day, Diary  # Dodaj te importy
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
async def send_message(message: ChatMessage):
    try:
        time.sleep(1)  # Dodaj 1 sekundę opóźnienia
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś pomocnym asystentem."},
                {"role": "user", "content": message.prompt}
            ]
        )
        ai_response = completion.choices[0].message.content
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