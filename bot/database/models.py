from sqlalchemy import Integer, String, Boolean, DateTime, Text, BigInteger, func, UUID
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base
from datetime import datetime, timezone
from utils import fk
from sqlalchemy.dialects.postgresql import UUID as pg_UUID


class User(Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    payment_status: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    promocode: Mapped[str] = mapped_column(Text, unique=True, nullable=True)
    promocode_usage_count: Mapped[int] = mapped_column(Integer, default=0)
    promocode_given: Mapped[bool] = mapped_column(Boolean, default=False)
    promocode_is_active: Mapped[str] = mapped_column(String(50), nullable=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=True)
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_check_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    achievement: Mapped[int] = mapped_column(Integer, default=1, nullable=True)


class Log(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, fk(User, "tg_id"), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    create_date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Payment(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, fk(User, "tg_id"), nullable=False)
    payment_id: Mapped[int] = mapped_column(pg_UUID, unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending", nullable=False)