from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

class ChatMessage(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

@router.post("/send", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
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