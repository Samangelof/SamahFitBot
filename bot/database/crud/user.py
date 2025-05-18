from sqlalchemy.orm import Session
from bot.database.models import User
from datetime import datetime


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
