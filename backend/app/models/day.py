from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, index=True)
    diary_id = Column(Integer, ForeignKey("diaries.id"), nullable=False)
    main_entry = Column(String, nullable=False)
    created_at = Column(Date, nullable=False)
    day_rating = Column(Integer, nullable=True)  # Dodaj tę linię

    diary = relationship("Diary", back_populates="days")