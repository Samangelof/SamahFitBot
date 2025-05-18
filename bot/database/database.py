from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .models import Base 


DATABASE_PATH = "sqlite:///samahfit.db"
engine = create_engine(DATABASE_PATH, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)

class DatabaseManager:
    def __init__(self):
        init_db()

    @contextmanager
    def session_scope(self):
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
