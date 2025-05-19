from sqlalchemy.orm import Session
from bot.database.models import UserAccess
from datetime import datetime, timedelta


def add_user_access(session: Session, user_id: int):
    access_end = datetime.utcnow() + timedelta(days=30)
    access = UserAccess(
        user_id=user_id,
        access_end=access_end,
        access_start=datetime.utcnow()
    )
    session.add(access)