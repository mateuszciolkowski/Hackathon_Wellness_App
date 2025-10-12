from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import diaries, days, questions_answers, avatars
from app.db.session import engine
from app.api.routes import chart, users
from app.api.models import Base

# Import wszystkich modeli, aby były zarejestrowane w Base.metadata
from app.api.models import User, Diary, Day, Avatar, Conversation, Message, QuestionAnswer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tabele zostały utworzone pomyślnie")
except Exception as e:
    logger.error(f"Błąd podczas tworzenia tabel: {e}")

app = FastAPI()

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji zastąp konkretnymi domenami
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(diaries.router)
app.include_router(days.router)
app.include_router(questions_answers.router)
app.include_router(avatars.router)

app.include_router(
    chart.router,
    prefix="/api",
    tags=["chart"]
)