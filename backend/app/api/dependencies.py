from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.models.user import User

# Stały token dla testów
TEST_TOKEN = "test_token_123"

async def get_current_user(
    token: str = Depends(lambda x: x.headers.get("Authorization")),
    db: Session = Depends(get_db)
) -> User:
    # Sprawdź, czy token jest poprawny
    if not token or token.replace("Bearer ", "") != TEST_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowy token autoryzacyjny"
        )

    # Pobierz użytkownika z bazy danych (możesz dostosować do swoich potrzeb)
    user = db.query(User).filter(User.id == 1).first()  # Zakładamy, że użytkownik o ID 1 istnieje
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Użytkownik nie znaleziony"
        )

    return user