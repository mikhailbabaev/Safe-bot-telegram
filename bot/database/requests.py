import uuid
from datetime import datetime, timezone
from sqlalchemy import select, cast, BigInteger, update
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from database.models import User, Log, Payment
from utils import generate_promocode
from templates import ACHIEVEMENT_LIST, ACTION_TEMPLATES


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


async def set_user_action(session: AsyncSession, tg_id: int, action: str):
    action_description = ACTION_TEMPLATES[action]


    # Печатаем все записи из таблицы users для проверки
    result = await session.execute(select(User))
    users = result.scalars().all()
    for user in users:
        print(f"tg_id: {user.tg_id}, first_name: {user.first_name}, last_name: {user.last_name}")

    # Создаем новую запись в таблице logs
    new_action = Log(
        user_id=tg_id,
        action=action_description,
        create_date_time=datetime.now(timezone.utc)
    )
    session.add(new_action)

    await session.commit()

async def save_payment(session: AsyncSession, tg_id: int, payment_id: str):
    """Сохраняем новый платеж в базе"""
    payment_uuid = uuid.UUID(payment_id)
    payment = Payment(user_id=tg_id, payment_id=payment_uuid, status="pending")
    session.add(payment)
    await session.commit()


async def get_unpaid_payments(session: AsyncSession):
    """Получаем список незавершённых платежей"""
    result = await session.execute(
        select(Payment.payment_id, Payment.user_id).where(Payment.status == "pending")
    )
    return result.fetchall()


async def update_payment_status(session: AsyncSession, payment_id: str, status: str):
    """Проверяем статус платежа по payment_id"""
    print(f'Функция проверки запущена для payment_id={payment_id}')

    # Преобразуем строку в UUID
    payment_id_uuid = UUID(payment_id)
    print(f'UUID: {payment_id_uuid}, type: {type(payment_id_uuid)}')

    query = select(Payment).where(Payment.payment_id == payment_id_uuid)
    result = await session.execute(query)

    # Получаем первую строку, если она есть
    payment = result.scalar_one_or_none()

    if payment:
        print(f'Запись найдена: {payment}')
        print(f'Текущий статус: {payment.status}')
    else:
        print(f'Запись с payment_id={payment_id_uuid} не найдена')