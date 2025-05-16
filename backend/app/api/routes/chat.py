from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from app.api.schemas import chat as schemas
from app.crud import chat as crud
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.api.models.user import User
import openai
import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

# Modele Pydantic do walidacji danych
class ChatMessage(BaseModel):
    prompt: str
    user_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str

# Endpoint: wysłanie wiadomości i utworzenie nowej konwersacji
@router.post("/send", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Utwórz nową konwersację
        conversation = crud.chat.create_conversation(db=db, user_id=current_user.id)

        # Zapisz wiadomość użytkownika
        crud.chat.create_message(
            db=db,
            conversation_id=conversation.id,
            content=message.prompt,
            role="user"
        )

        # Wygeneruj odpowiedź AI
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Jesteś pomocnym asystentem."},
                    {"role": "user", "content": message.prompt}
                ]
            )
            ai_response = completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Błąd podczas komunikacji z OpenAI: {str(e)}"
            )

        # Zapisz odpowiedź AI
        crud.chat.create_message(
            db=db,
            conversation_id=conversation.id,
            content=ai_response,
            role="assistant"
        )

        return ChatResponse(response=ai_response)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas przetwarzania wiadomości: {str(e)}"
        )

# Endpoint: tworzenie pustej konwersacji
@router.post("/conversations", response_model=schemas.ConversationResponse)
async def create_conversation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.chat.create_conversation(db=db, user_id=current_user.id)

# Endpoint: wysyłanie wiadomości w istniejącej konwersacji
@router.post("/conversations/{conversation_id}/messages", response_model=schemas.MessageResponse)
async def send_message_to_existing_conversation(
    conversation_id: int,
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        conversation = crud.chat.get_conversation(db, conversation_id)
        if not conversation or conversation.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Konwersacja nie znaleziona")

        # Zapisz wiadomość użytkownika
        crud.chat.create_message(
            db=db,
            conversation_id=conversation_id,
            content=message.content,
            role="user"
        )

        # Wygeneruj odpowiedź AI
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Jesteś pomocnym asystentem."},
                    {"role": "user", "content": message.content}
                ]
            )
            ai_response = completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Błąd podczas komunikacji z OpenAI: {str(e)}"
            )

        # Zapisz odpowiedź AI
        assistant_message = crud.chat.create_message(
            db=db,
            conversation_id=conversation_id,
            content=ai_response,
            role="assistant"
        )

        return assistant_message

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Wystąpił błąd podczas przetwarzania wiadomości: {str(e)}"
        )

# Endpoint: pobranie listy konwersacji użytkownika
@router.get("/conversations", response_model=List[schemas.ConversationResponse])
async def get_user_conversations(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.chat.get_user_conversations(db=db, user_id=current_user.id, skip=skip, limit=limit)