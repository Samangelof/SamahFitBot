from sqlalchemy.orm import Session
from bot.database.models import Referral, User


def mark_referral_paid(session: Session, invited_telegram_id: int):
    invited_user = session.query(User).filter_by(telegram_id=invited_telegram_id).first()
    if not invited_user:
        return

    session.query(Referral)\
        .filter_by(invited_user_id=invited_user.id)\
        .update({"paid": True})


def add_referral(session: Session, inviter_telegram_id: int, invited_telegram_id: int):
    if inviter_telegram_id == invited_telegram_id:
        return  # Сам себя пригласил — игнорируем

    inviter = session.query(User).filter_by(telegram_id=inviter_telegram_id).first()
    invited = session.query(User).filter_by(telegram_id=invited_telegram_id).first()

    if not inviter or not invited:
        return

    exists = session.query(Referral).filter_by(
        user_id=inviter.id,
        invited_user_id=invited.id
    ).first()

    if exists:
        return  # Уже записан

    referral = Referral(user_id=inviter.id, invited_user_id=invited.id)
    session.add(referral)


def get_referral_count(session: Session, telegram_id: int) -> int:
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        return 0

    return session.query(Referral).filter_by(user_id=user.id, paid=True).count()

def get_discount_percent(session: Session, telegram_id: int) -> int:
    count = get_referral_count(session, telegram_id)
    if count >= 2:
        return 50
    elif count == 1:
        return 25
    return 0
