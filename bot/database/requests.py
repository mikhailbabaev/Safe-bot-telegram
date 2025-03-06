from datetime import datetime, timezone
from sqlalchemy import select, cast, BigInteger, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from utils import generate_promocode
from templates import ACHIEVEMENT_LIST


async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User | None:
    """Существует ли пользователь с таким tg_id"""
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    return result.scalars().first()


async def create_user(
        session: AsyncSession,
        tg_id: int,
        first_name: str,
        last_name: str | None,
        username: str | None,
        is_bot: bool
):
    """Функция для создания нового пользователя"""
    promocode = generate_promocode(tg_id)

    new_user = User(
        tg_id=tg_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        promocode=promocode,
        is_bot=is_bot
    )
    session.add(new_user)
    await session.commit()


async def get_promocode_by_tg_id(session: AsyncSession, tg_id: int) -> str:
    result = await session.execute(select(User.promocode).filter(User.tg_id == tg_id))
    promocode = result.scalar()
    return promocode


async def set_promocode_given(session: AsyncSession, tg_id: int):
    stmt = update(User).where(User.tg_id == tg_id).values(promocode_given=True)
    await session.execute(stmt)
    await session.commit()


async def set_promocode_usage(session: AsyncSession, tg_id: int, promocode: str):
    # Ищем запись о пользователе с указанным промокодом
    result = await session.execute(select(User).where(User.promocode == promocode))
    promocode_entry = result.scalar_one_or_none()  # Получаем запись или None, если не найдено

    if not promocode_entry:  # Если промокод не найден
        return False

    stmt = (
        update(User)
        .where(User.tg_id == tg_id)
        .values(promocode_usage_count=User.promocode_usage_count + 1)
    )
    await session.execute(stmt)
    await session.commit()
    return True



async def get_tg_id_by_promocode(session: AsyncSession, promocode: str):
    stmt = select(User.tg_id).filter(User.promocode == promocode)
    result = await session.execute(stmt)
    tg_id = result.scalars().first()
    return tg_id


async def set_promocode_is_active(session: AsyncSession, tg_id: int, promocode: str):
    stmt = update(User).where(User.tg_id == tg_id).values(promocode_is_active=promocode)
    await session.execute(stmt)
    await session.commit()


async def check_promocode_is_active(session: AsyncSession, tg_id: int):
    stmt = select(User.promocode_is_active).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    promocode_is_active = result.scalars().first()
    if promocode_is_active:
        return True
    else:
        return False


async def set_last_check_time(session: AsyncSession, tg_id: int):
    stmt = update(User).where(User.tg_id == tg_id).values(last_check_date=datetime.now(timezone.utc))
    await session.execute(stmt)
    await session.commit()


async def set_payment_time(session: AsyncSession, tg_id: int):
    stmt = (
        update(User)
        .where(User.tg_id == tg_id)
        .values(payment_date=datetime.now(timezone.utc))
    )
    await session.execute(stmt)
    await session.commit()


async def get_user_achievement_text(session: AsyncSession, tg_id: int) -> str:
    """Создает клавиатуру с достижением пользователя."""
    stmt = select(User.achievement).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    achievement = result.scalar()

    achievement_text = ACHIEVEMENT_LIST.get(achievement)
    return achievement_text
