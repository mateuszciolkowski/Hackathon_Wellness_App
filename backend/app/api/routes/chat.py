from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import openai
import os

router = APIRouter()

# Wczytanie zmiennych środowiskowych z .env (jeśli używasz python-dotenv)
# from dotenv import load_dotenv
# load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str

@router.post("/send", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś pomocnym asystentem."},
                {"role": "user", "content": message.message}
            ]
        )
        ai_response = response.choices[0].message.content
        return ChatResponse(response=ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas komunikacji z ChatGPT: {str(e)}")