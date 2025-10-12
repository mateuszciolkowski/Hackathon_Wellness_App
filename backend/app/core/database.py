from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import logging
import os

# Konfiguracja loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WERSJA DLA DOCKER COMPOSE: Używa nazwy serwisu 'db' i pobiera dane z zmiennych środowiskowych
# Używamy tej zmiennej ZAWSZE, gdy działa Docker Compose.
# W Twoim pliku .env masz: POSTGRES_DB=postgres
# W Twoim backendzie jest błąd, bo próbujesz połączyć się z 'wellness_db'.
# Upewniamy się, że domyślny adres wskazuje na poprawnie utworzoną bazę 'postgres'.
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@db:5432/postgres"
)
SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = None 
Base = declarative_base() # Definicja Base musi być globalna

# --- Inicjalizacja Połączenia i Fallback ---
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Próba nawiązania połączenia
    engine.connect()
    logger.info("Połączenie z bazą danych PostgreSQL zostało ustanowione pomyślnie")
    
    # TUTAJ TRZEBA DODAĆ Base.metadata.create_all(bind=engine) PO ZAIMPORTOWANIU MODELI
    
except OperationalError as e:
    logger.error(f"Nie można połączyć się z bazą danych: {str(e)}")
    # Logika fallbacku jest ZACHOWANA dla odporności na błędy
    logger.warning("Używam bazy danych SQLite w pamięci jako fallback")
    engine = create_engine('sqlite:///:memory:')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generator sesji bazy danych (Dependency Injection)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()