from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from bot.database.models import User


def get_by_telegram_id(session: Session, telegram_id: int) -> User | None:
    return session.query(User).filter_by(telegram_id=telegram_id).first()


def create(session: Session, tg_user) -> User:
    user = User(
        telegram_id=tg_user.id,
        username=tg_user.username,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
        language_code=tg_user.language_code,
        registration_date=datetime.utcnow()
    )
    session.add(user)
    return user


def get_or_create(session: Session, tg_user) -> User:
    user = get_by_telegram_id(session, tg_user.id)
    if user is None:
        user = create(session, tg_user)
    return user



def add_or_update_user(
    session: Session,
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    language_code: Optional[str] = None) -> int:
    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    if user:
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.language_code = language_code
        # регистрация уже есть — не трогаем
    else:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            language_code=language_code,
            registration_date=datetime.utcnow()
        )
        session.add(user)
        session.flush()  # чтобы получить user.id

    return user.id
