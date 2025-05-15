from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    registration_date = Column(DateTime, server_default=func.now())

    applications = relationship("Application", back_populates="user")
    accesses = relationship("UserAccess", back_populates="user")
    invited_referrals = relationship("Referral", foreign_keys='Referral.user_id', back_populates="inviter")
    received_referrals = relationship("Referral", foreign_keys='Referral.invited_user_id', back_populates="invited")


class UserAccess(Base):
    __tablename__ = 'user_access'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    access_start = Column(DateTime, server_default=func.now())
    access_end = Column(DateTime)

    user = relationship("User", back_populates="accesses")


class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    answers = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    payment_status = Column(String, default='не оплачено')
    payment_id = Column(String)
    payment_date = Column(DateTime)

    user = relationship("User", back_populates="applications")


class UserVisit(Base):
    __tablename__ = 'user_visits'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    visit_time = Column(DateTime, server_default=func.now())


class Referral(Base):
    __tablename__ = 'referrals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    invited_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    discount_applied = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    inviter = relationship("User", foreign_keys=[user_id], back_populates="invited_referrals")
    invited = relationship("User", foreign_keys=[invited_user_id], back_populates="received_referrals")
