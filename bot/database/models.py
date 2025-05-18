from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, TIMESTAMP, Boolean
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    registration_date = Column(TIMESTAMP, default=datetime.utcnow)

    access = relationship('UserAccess', back_populates='user', cascade='all, delete-orphan')
    applications = relationship('Application', back_populates='user', cascade='all, delete-orphan')
    invited_by = relationship('Referral', back_populates='invited_user', foreign_keys='Referral.invited_user_id', cascade='all, delete-orphan')
    referrals = relationship('Referral', back_populates='user', foreign_keys='Referral.user_id', cascade='all, delete-orphan')


class UserAccess(Base):
    __tablename__ = 'user_access'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    access_start = Column(TIMESTAMP, default=datetime.utcnow)
    access_end = Column(TIMESTAMP)

    user = relationship('User', back_populates='access')


class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    answers = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    payment_status = Column(String, default='не оплачено')
    payment_id = Column(String)
    payment_url = Column(String)
    payment_date = Column(TIMESTAMP)

    user = relationship('User', back_populates='applications')


class UserVisit(Base):
    __tablename__ = 'user_visits'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    visit_time = Column(TIMESTAMP, default=datetime.utcnow)


class Referral(Base):
    __tablename__ = 'referrals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Кто пригласил
    invited_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Кого пригласили
    paid = Column(Boolean, default=False)
    discount_applied = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship('User', back_populates='referrals', foreign_keys=[user_id])
    invited_user = relationship('User', back_populates='invited_by', foreign_keys=[invited_user_id])


class PromoCode(Base):
    __tablename__ = 'promocodes'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    discount_percent = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
