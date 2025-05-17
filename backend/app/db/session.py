from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging
from sqlalchemy.exc import OperationalError

# Konfiguracja loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@127.0.0.1:5432/mental"

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