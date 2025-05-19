from sqlalchemy.orm import Session
from typing import Optional, List
import json
from datetime import datetime
from bot.database.models import Application, User



def get_application_by_id(session: Session, application_id: int) -> Optional[dict]:
    app = (
        session.query(Application)
        .join(User)
        .filter(Application.id == application_id)
        .first()
    )
    if not app:
        return None

    return {
        "id": app.id,
        "user_id": app.user_id,
        "answers": json.loads(app.answers),
        "created_at": app.created_at,
        "payment_status": app.payment_status,
        "payment_id": app.payment_id,
        "payment_url": app.payment_url,
        "payment_date": app.payment_date,
        "telegram_id": app.user.telegram_id,
        "username": app.user.username,
        "first_name": app.user.first_name,
        "last_name": app.user.last_name,
    }


def get_user_applications(session: Session, telegram_id: int) -> List[dict]:
    apps = (
        session.query(Application)
        .join(User)
        .filter(User.telegram_id == telegram_id)
        .order_by(Application.created_at.desc())
        .all()
    )
    return [
        {
            "id": app.id,
            "user_id": app.user_id,
            "answers": json.loads(app.answers),
            "created_at": app.created_at,
            "payment_status": app.payment_status,
            "payment_id": app.payment_id,
            "payment_url": app.payment_url,
            "payment_date": app.payment_date,
        }
        for app in apps
    ]


def get_telegram_id_by_application_id(session: Session, application_id: int) -> Optional[int]:
    app = (
        session.query(Application)
        .join(User)
        .filter(Application.id == application_id)
        .first()
    )
    if not app:
        return None
    return app.user.telegram_id

def save_application(session: Session, telegram_id: int, answers: dict) -> int:
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        print(f"[save_application] Пользователь с telegram_id {telegram_id} не найден в базе")
        return 0

    app = Application(
        user_id=user.id,
        answers=json.dumps(answers, ensure_ascii=False),
    )
    session.add(app)
    session.flush()  # чтобы получить app.id до коммита

    return app.id



def update_payment_url(session: Session, application_id: int, payment_url: str):
    session.query(Application)\
        .filter_by(id=application_id)\
        .update({"payment_url": payment_url})



def update_payment_status(
    session: Session,
    application_id: int,
    payment_status: str,
    payment_id: Optional[str] = None,
    add_access_callback=None,
    mark_referral_callback=None
) -> bool:
    try:
        now = datetime.utcnow()
        app = session.query(Application).filter_by(id=application_id).first()
        if not app:
            return False

        app.payment_status = payment_status
        app.payment_id = payment_id

        if payment_status == "оплачено":
            app.payment_date = now

            # даем доступ пользователю
            if add_access_callback:
                add_access_callback(session, app.user_id)

            # помечаем рефералку оплаченной
            if mark_referral_callback:
                telegram_id = app.user.telegram_id
                mark_referral_callback(session, telegram_id)

        return True
    except Exception as e:
        print(f"[update_payment_status] Ошибка: {e}")
        return False
