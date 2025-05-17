from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Avatar(Base):
    __tablename__ = "avatars"

    id = Column(Integer, primary_key=True, index=True)
    diary_id = Column(Integer, ForeignKey("diaries.id", ondelete="CASCADE"), unique=True, nullable=False)

    diary = relationship("Diary", back_populates="avatar", lazy="joined")