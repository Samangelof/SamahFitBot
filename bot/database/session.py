from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from bot.database.models import Base
import os


DB_PATH = os.getenv("DB_PATH", "sqlite:///bot_database.sqlite3")


engine = create_engine(DB_PATH, echo=False, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(bind=engine))


def init_db():
    Base.metadata.create_all(bind=engine)
