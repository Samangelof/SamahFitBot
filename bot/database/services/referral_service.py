from sqlalchemy.orm import Session
from bot.database.models import Referral, User
from typing import Optional


class ReferralService:
    def __init__(self, db: Session):
        self.db = db

    def add_referral(self, inviter_tg_id: int, invited_tg_id: int):
        inviter = self.db.query(User).filter_by(telegram_id=inviter_tg_id).first()
        invited = self.db.query(User).filter_by(telegram_id=invited_tg_id).first()

        if not inviter or not invited:
            return

        exists = self.db.query(Referral).filter_by(user_id=inviter.id, invited_user_id=invited.id).first()
        if exists:
            return

        referral = Referral(user_id=inviter.id, invited_user_id=invited.id)
        self.db.add(referral)
        self.db.commit()

    def get_referral_count(self, telegram_id: int) -> int:
        user = self.db.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            return 0

        return self.db.query(Referral).filter_by(user_id=user.id).count()

    def get_discount_percent(self, telegram_id: int) -> int:
        count = self.get_referral_count(telegram_id)
        if count >= 2:
            return 50
        elif count == 1:
            return 25
        return 0
