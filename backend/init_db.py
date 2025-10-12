# backend/init_db.py

import sys
import time
import logging

# Importuje obiekty Base i engine z pliku połączeniowego
# Zmień ścieżkę 'app.db.session' na właściwą, jeśli Twoja struktura jest inna (np. 'core.database')
from app.db.session import Base, engine 
# Musisz zaimportować WSZYSTKIE MODELE, aby SQLAlchemy wiedziało, jakie tabele stworzyć
import app.api.models 

logger = logging.getLogger("db_initializer")
logging.basicConfig(level=logging.INFO)

def init_db_schema(max_retries=15, delay=3):
    """
    Tworzy schemę bazy danych PostgreSQL.
    Ponawia próbę, aby obsłużyć opóźnienia w starcie serwera DB.
    """
    logger.info("Rozpoczęto synchronizację schemy bazy danych.")
    
    for i in range(max_retries):
        try:
            # Wymuszenie tworzenia tabel - KLUCZOWY KROK
            Base.metadata.create_all(bind=engine)
            logger.info("Sukces: Schemat bazy danych (tabele) jest gotowy.")
            return True
        except Exception as e:
            # Łapanie błędów (np. OperationalError), jeśli baza danych jest niedostępna lub zajęta
            logger.warning(f"Błąd tworzenia tabel (Próba {i+1}/{max_retries}). Czekam {delay}s. Błąd: {e}")
            time.sleep(delay)
    
    logger.error("Nie udało się utworzyć schemy po wszystkich próbach. KOŃCZENIE PRACY.")
    return False

if __name__ == "__main__":
    if init_db_schema():
        sys.exit(0) # Pomyślne zakończenie: Docker przejdzie do następnej komendy
    else:
        sys.exit(1) # Błąd: Kontener zostanie zatrzymany