from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from bot.database.models import User
from typing import Optional
from aiogram.types import User as TelegramUser


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def add_user_if_not_exists(self, tg_user: TelegramUser):
        user = self.db.query(User).filter_by(telegram_id=tg_user.id).first()
        if not user:
            user = User(
                telegram_id=tg_user.id,
                username=tg_user.username,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                language_code=tg_user.language_code
            )
            self.db.add(user)
            try:
                self.db.commit()
            except IntegrityError:
                self.db.rollback()