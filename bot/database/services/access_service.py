from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from bot.database.models import UserAccess


class AccessService:
    def __init__(self, db: Session):
        self.db = db

    def add_access(self, user_id: int):
        access_end = datetime.utcnow() + timedelta(days=30)
        access = UserAccess(user_id=user_id, access_end=access_end)
        self.db.add(access)
        self.db.commit()

    def check_access(self, user_id: int) -> bool:
        access = (
            self.db.query(UserAccess)
            .filter(UserAccess.user_id == user_id, UserAccess.access_end > datetime.utcnow())
            .order_by(UserAccess.access_end.desc())
            .first()
        )
        return access is not None
