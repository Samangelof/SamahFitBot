from sqlalchemy.orm import Session
from sqlalchemy import func
from bot.database.models import UserVisit
from aiogram.types import User as TelegramUser
from typing import List, Tuple


class VisitService:
    def __init__(self, db: Session):
        self.db = db

    def log_user_visit(self, user: TelegramUser):
        visit = UserVisit(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        self.db.add(visit)
        self.db.commit()

    def get_daily_visits(self) -> List[Tuple[str, int]]:
        result = (
            self.db.query(func.date(UserVisit.visit_time), func.count())
            .group_by(func.date(UserVisit.visit_time))
            .order_by(func.date(UserVisit.visit_time).desc())
            .limit(30)
            .all()
        )
        return result

    def get_unique_user_count(self) -> int:
        return self.db.query(func.count(func.distinct(UserVisit.telegram_id))).scalar()