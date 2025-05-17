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

origins = [
    "http://localhost:3000/",
    "http://127.0.0.1:3000/",
    "*"  # UWAGA: pozwala na wszystko (OK w dev, nie w produkcji)
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,            # Skąd można się łączyć
#     allow_credentials=True,
#     allow_methods=["*"],              # Jakie metody są dozwolone (GET, POST, itd.)
#     allow_headers=["*"],              # Jakie nagłówki są dozwolone (np. Authorization)
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=[
    #     "http://localhost:3000",
    #     "http://127.0.0.1:3000",
    #     "https://tg4n8lh6-8000.euw.devtunnels.ms",  # ← dodaj DevTunnel jako origin
    # ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age = 3600
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
    uvicorn.run(app, host="0.0.0.0", port=3000)