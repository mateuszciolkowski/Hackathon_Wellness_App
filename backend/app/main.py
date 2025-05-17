from fastapi import FastAPI
from app.api import users, diaries, days, questions_answers, avatars
from app.db.session import engine, Base
from app.api.routes import chart

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(diaries.router)
app.include_router(days.router)
app.include_router(questions_answers.router)
app.include_router(avatars.router)

app.include_router(
    chart.router,
    prefix="/api",
    tags=["chart"]
)