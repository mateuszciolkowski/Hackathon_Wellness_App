from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Diary(Base):
    __tablename__ = "diaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="diaries")
    days = relationship("Day", back_populates="diary", cascade="all, delete")
    avatar = relationship("Avatar", back_populates="diary", uselist=False, cascade="all, delete")