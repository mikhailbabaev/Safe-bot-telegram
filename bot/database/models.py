from sqlalchemy import Integer, String, Boolean, DateTime, Text, BigInteger, func, Float
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base
from datetime import datetime
from utils import fk


class User(Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_bot: Mapped[bool] = mapped_column(Boolean, default=True)
    last_check_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    check_percent: Mapped[int] = mapped_column(Integer, nullable=True)
    check_text_number: Mapped[int] = mapped_column(Integer, nullable=True)
    achievement: Mapped[int] = mapped_column(Integer, default=1, nullable=True)
    payment_status: Mapped[bool] = mapped_column(Boolean, default=False)
    payment_end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    wallet_rub: Mapped[float] = mapped_column(Float, default=0.0)
    promocode: Mapped[str] = mapped_column(Text, unique=True, nullable=True)
    promocode_usage_count: Mapped[int] = mapped_column(Integer, default=0)
    promocode_given: Mapped[bool] = mapped_column(Boolean, default=False)
    promocode_is_active: Mapped[str] = mapped_column(String(50), nullable=True)


class Log(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, fk(User, "tg_id"), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    create_date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Payment(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, fk(User, "tg_id"), nullable=False)
    payment_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending", nullable=False)
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class SecurityStepProgress(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, fk(User, "tg_id"), nullable=False)
    step_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())