import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import users, diaries, days, chat, questions_answers, chart  # dodano import chart
from app.db.session import engine, Base
import logging

logger = logging.getLogger(__name__)

# Tworzymy wszystkie tabele w bazie danych
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tabele zostały utworzone pomyślnie")
except Exception as e:
    logger.error(f"Błąd podczas tworzenia tabel: {str(e)}")



app = FastAPI(
    title="Diary API",
    description="API do zarządzania dziennikiem",
    version="1.0.0"
)

FRONTEND_HTTP = os.getenv("FRONTEND_URL_HTTP", "")
FRONTEND_HTTPS = os.getenv("FRONTEND_URL_HTTPS", "")

LOCAL_HTTP = "http://localhost:3001"
LOCAL_IP = "http://127.0.0.1:3001" 

origins = [
    origin for origin in [FRONTEND_HTTP, FRONTEND_HTTPS, LOCAL_HTTP, LOCAL_IP] if origin
]

origins_normalized = set()
for url in origins:
    origins_normalized.add(url)
    if url.endswith('/'):
         origins_normalized.add(url[:-1])



app.add_middleware(
    CORSMiddleware,
    allow_origins=list(origins_normalized), # Przekazanie listy unikalnych domen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Podpinamy routery
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(diaries.router, prefix="/api/diaries", tags=["diaries"])
app.include_router(days.router, prefix="/api/days", tags=["days"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(questions_answers.router, prefix="/api/questions_answers", tags=["questions_answers"])
app.include_router(chart.router, prefix="/api/chart", tags=["chart"])  # dodano nowy router

@app.get("/")
def read_root():
    return {"message": "Witaj w API Dziennika"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)