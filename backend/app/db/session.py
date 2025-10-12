# backend/db/session.py lub backend/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import logging
import os

# Konfiguracja loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 1. Konfiguracja i Inicjalizacja Silnika ---

# ODBIÓR DANYCH Z DOCKER COMPOSE: Zawsze używamy wewnętrznej nazwy serwisu 'db'
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@db:5432/postgres" # Wartość domyślna zgodna z Twoim Docker Compose
)
SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = None 
Base = declarative_base() # Klasa bazowa dla wszystkich modeli ORM

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Próba nawiązania połączenia (sprawdzenie, czy serwer DB działa)
    engine.connect() 
    logger.info("Połączenie z bazą danych PostgreSQL zostało ustanowione pomyślnie")
    
except OperationalError as e:
    logger.error(f"Nie można połączyć się z bazą danych PostgreSQL: {str(e)}")
    
    # Logika fallbacku: Używana, gdy PostgreSQL jest niedostępny
    logger.warning("Używam bazy danych SQLite w pamięci jako fallback")
    engine = create_engine('sqlite:///:memory:')

# --- 2. Konfiguracja Sesji ---

# Tworzenie klasy lokalnej sesji powiązanej z silnikiem (PostgreSQL lub SQLite)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# --- 3. Funkcja Dependency Injection ---

def get_db():
    """Dostarcza sesję bazy danych do endpointów FastAPI."""
    db = SessionLocal()
    try:
        yield db # Zwraca sesję do użycia
    finally:
        db.close() # Zawsze zamyka sesję po obsłużeniu żądania