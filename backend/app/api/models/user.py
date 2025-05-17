from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    nickname = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=False)

    diaries = relationship("Diary", back_populates="user", cascade="all, delete")
    
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete")