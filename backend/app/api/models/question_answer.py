# podawane sa trzy pytania do uzytkownika
#uzytkownik odpowiada na te pytania
#w bd zapisywane sa pytania
#w bazie danych sa zapisywane odpowiedzi na te pytania
#zapis konwersacji na potrzeby generacji odpowiedzi i analizy kontekstu
#pytanie jest kolumna w QA
#odp jest kolumna w QA
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class QuestionAnswer(Base):
    __tablename__ = "questions_answers"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text)

    day = relationship("Day", back_populates="questions_answers")


