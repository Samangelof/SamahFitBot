from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func
from bot.database.models import UserVisit


def get_daily_visits(session: Session, limit: int = 30) -> list[tuple[str, int]]:
    result = (
        session.query(
            func.date(UserVisit.visit_time).label("visit_date"),
            func.count().label("visit_count")
        )
        .group_by("visit_date")
        .order_by("visit_date DESC")
        .limit(limit)
        .all()
    )
    return result  # вернет кортеж: [(дата, кол-во), ...]



def get_unique_user_count(session: Session) -> int:
    return session.query(func.count(func.distinct(UserVisit.telegram_id))).scalar()


def log_visit(session: Session, tg_user):
    visit = UserVisit(
        telegram_id=tg_user.id,
        username=tg_user.username,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
        visit_time=datetime.utcnow()
    )
    session.add(visit)

