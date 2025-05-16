from sqlalchemy.orm import Session
from app.api.models.conversation import Conversation, Message
from app.api.schemas import chat as schemas

def create_conversation(db: Session, user_id: int):
    db_conversation = Conversation(user_id=user_id)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def create_message(db: Session, conversation_id: int, content: str, role: str):
    db_message = Message(
        conversation_id=conversation_id,
        content=content,
        role=role
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_conversation(db: Session, conversation_id: int):
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def get_user_conversations(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Conversation).filter(Conversation.user_id == user_id).offset(skip).limit(limit).all()