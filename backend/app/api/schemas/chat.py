from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .base import BaseSchema

class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase, BaseSchema):
    id: int
    conversation_id: int
    created_at: datetime

class ConversationBase(BaseModel):
    user_id: int

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase, BaseSchema):
    id: int
    created_at: datetime
    messages: List[MessageResponse] = []