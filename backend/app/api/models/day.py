from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import date
from .base import Base

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, index=True)
    diary_id = Column(Integer, ForeignKey("diaries.id", ondelete="CASCADE"), nullable=False)
    main_entry = Column(Text)
    created_at = Column(Date, default=date.today)
    day_rating = Column(Integer) 
    
    diary = relationship("Diary", back_populates="days")
    questions_answers = relationship("QuestionAnswer", back_populates="day", cascade="all, delete")


    