from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging
from sqlalchemy.exc import OperationalError
import os

# Konfiguracja loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pobierz URL bazy danych z zmiennej środowiskowej lub użyj domyślnego
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")
SQLALCHEMY_DATABASE_URL = DATABASE_URL

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Próba nawiązania połączenia
    engine.connect()
    logger.info("Połączenie z bazą danych zostało ustanowione pomyślnie")
except OperationalError as e:
    logger.error(f"Nie można połączyć się z bazą danych: {str(e)}")
    # Tworzymy silnik SQLite w pamięci jako fallback
    logger.warning("Używam bazy danych SQLite w pamięci jako fallback")
    engine = create_engine('sqlite:///:memory:')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()