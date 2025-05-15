from sqlalchemy.orm import Session
from sqlalchemy import desc
from bot.database.models import User, Application
from bot.database.services.access_service import AccessService
from datetime import datetime
from typing import Dict, Optional, List
import json


class ApplicationService:
    def __init__(self, db: Session):
        self.db = db

    def save_application(self, telegram_id: int, answers: Dict) -> int:
        user = self.db.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            return 0

        application = Application(user_id=user.id, answers=json.dumps(answers, ensure_ascii=False))
        self.db.add(application)
        self.db.commit()
        return application.id

    def update_payment_status(self, application_id: int, payment_status: str, payment_id: Optional[str] = None) -> bool:
        app = self.db.query(Application).filter_by(id=application_id).first()
        if not app:
            return False

        app.payment_status = payment_status
        app.payment_id = payment_id
        if payment_status == 'оплачено':
            app.payment_date = datetime.utcnow()
            AccessService(self.db).add_access(app.user_id)

        self.db.commit()
        return True

    def get_application_by_id(self, application_id: int) -> Optional[Dict]:
        app = (
            self.db.query(Application)
            .join(User)
            .filter(Application.id == application_id)
            .with_entities(Application, User.telegram_id, User.username, User.first_name, User.last_name)
            .first()
        )
        if not app:
            return None

        application, tg_id, username, first_name, last_name = app
        data = {
            "id": application.id,
            "answers": json.loads(application.answers),
            "created_at": application.created_at,
            "payment_status": application.payment_status,
            "payment_id": application.payment_id,
            "payment_date": application.payment_date,
            "telegram_id": tg_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name
        }
        return data

    def get_user_applications(self, telegram_id: int) -> List[Dict]:
        user = self.db.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            return []

        apps = (
            self.db.query(Application)
            .filter_by(user_id=user.id)
            .order_by(desc(Application.created_at))
            .all()
        )
        return [
            {
                "id": a.id,
                "answers": json.loads(a.answers),
                "created_at": a.created_at,
                "payment_status": a.payment_status,
                "payment_id": a.payment_id,
                "payment_date": a.payment_date
            }
            for a in apps
        ]

    def get_telegram_id_by_application_id(self, application_id: int) -> Optional[int]:
        app = (
            self.db.query(Application)
            .join(User)
            .filter(Application.id == application_id)
            .with_entities(User.telegram_id)
            .first()
        )
        return app[0] if app else None
