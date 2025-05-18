from sqlalchemy.orm import Session
from bot.database.models import UserVisit
from datetime import datetime


def log_visit(session: Session, tg_user):
    visit = UserVisit(
        telegram_id=tg_user.id,
        username=tg_user.username,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
        visit_time=datetime.utcnow()
    )
    session.add(visit)

