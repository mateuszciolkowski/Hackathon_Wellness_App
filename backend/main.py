from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import users, diaries, days
from app.core.database import engine
from app.api.models.base import Base

# Tworzymy wszystkie tabele w bazie danych
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Diary API",
    description="API do zarządzania dziennikiem",
    version="1.0.0"
)

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Podpinamy routery
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(diaries.router, prefix="/api/diaries", tags=["diaries"])
app.include_router(days.router, prefix="/api/days", tags=["days"])

@app.get("/")
def read_root():
    return {"message": "Witaj w API Dziennika"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)