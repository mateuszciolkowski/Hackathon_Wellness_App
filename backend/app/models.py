from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    nickname = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    birth_year = Column(Integer, nullable=False)

    diary = relationship("Diary", back_populates="user", uselist=False)

class Diary(Base):
    __tablename__ = "diaries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="diary")
    days = relationship("Day", back_populates="diary")
    avatar = relationship("Avatar", back_populates="diary", uselist=False)

class Day(Base):
    __tablename__ = "days"
    id = Column(Integer, primary_key=True, index=True)
    diary_id = Column(Integer, ForeignKey("diaries.id", ondelete="CASCADE"), nullable=False)
    main_entry = Column(Text)
    created_at = Column(Date, nullable=False)

    diary = relationship("Diary", back_populates="days")
    questions_answers = relationship("QuestionAnswer", back_populates="day")

class QuestionAnswer(Base):
    __tablename__ = "questions_answers"
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text)

    day = relationship("Day", back_populates="questions_answers")

class Avatar(Base):
    __tablename__ = "avatars"
    id = Column(Integer, primary_key=True, index=True)
    diary_id = Column(Integer, ForeignKey("diaries.id", ondelete="CASCADE"), unique=True, nullable=False)

    diary = relationship("Diary", back_populates="avatar")