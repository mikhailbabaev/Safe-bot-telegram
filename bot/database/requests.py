import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Log, Payment, SecurityStepProgress
from utils import generate_promocode
from templates import ACTION_TEMPLATES

logger = logging.getLogger(__name__)


async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> Optional[User]:
    """Существует ли пользователь с таким tg_id."""
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    user = result.scalars().first()
    logger.info(f"get_user_by_tg_id: {tg_id} - {user if user else 'не найден'}")
    return user


async def create_user(
    session: AsyncSession,
    tg_id: int,
    first_name: str,
    last_name: Optional[str],
    username: Optional[str],
    is_bot: bool
) -> None:
    """Функция для создания нового пользователя."""
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
    logger.info(f"create_user: новый пользователь с tg_id={tg_id} создан")


async def get_promocode_by_tg_id(session: AsyncSession, tg_id: int) -> str:
    """Получить промокод по телеграмм_id."""
    result = await session.execute(select(User.promocode).filter(User.tg_id == tg_id))
    promocode: str = result.scalar()
    logger.info(f"get_promocode_by_tg_id: tg_id={tg_id}, найден промокод={promocode}")
    return promocode


async def set_promocode_given(session: AsyncSession, tg_id: int) -> None:
    """Включить флажок, что промокод выдан."""
    stmt = update(User).where(User.tg_id == tg_id).values(promocode_given=True)
    await session.execute(stmt)
    await session.commit()
    logger.info(f"set_promocode_given: tg_id={tg_id}, флаг promocode_given установлен")


async def set_promocode_usage(session: AsyncSession, tg_id: int, promocode: str) -> bool:
    """Прибавить счетчик, что промокод использован."""
    result = await session.execute(select(User).where(User.promocode == promocode))
    promocode_entry = result.scalar_one_or_none()

    if not promocode_entry:
        logger.info(f"set_promocode_usage: tg_id={tg_id}, промокод {promocode} не найден")
        return False

    stmt = (
        update(User)
        .where(User.tg_id == tg_id)
        .values(promocode_usage_count=User.promocode_usage_count + 1)
    )
    await session.execute(stmt)
    await session.commit()
    logger.info(f"set_promocode_usage: tg_id={tg_id}, использован промокод {promocode}")
    return True


async def get_tg_id_by_promocode(session: AsyncSession, promocode: str) -> Optional[int]:
    """Получить телеграмм_id по промокоду."""
    stmt = select(User.tg_id).filter(User.promocode == promocode)
    result = await session.execute(stmt)
    tg_id: Optional[int] = result.scalars().first()
    logger.info(f"get_tg_id_by_promocode: найден tg_id={tg_id} для промокода {promocode}")
    return tg_id


async def set_promocode_is_active(session: AsyncSession, tg_id: int, promocode: str) -> None:
    """Флажок, установлен ли промокод."""
    stmt = update(User).where(User.tg_id == tg_id).values(promocode_is_active=promocode)
    await session.execute(stmt)
    await session.commit()
    logger.info(f"set_promocode_is_active: tg_id={tg_id}, активирован промокод {promocode}")


async def check_promocode_is_active(session: AsyncSession, tg_id: int) -> bool:
    """Проверить, активен ли промокод пользователя."""
    stmt = select(User.promocode_is_active).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    promocode_is_active = result.scalars().first()
    logger.info(f"check_promocode_is_active: tg_id={tg_id}, промокод активен={bool(promocode_is_active)}")
    return bool(promocode_is_active)


async def set_last_check_time(session: AsyncSession, tg_id: int) -> None:
    """Дата последней проверки."""
    stmt = update(User).where(User.tg_id == tg_id).values(last_check_date=datetime.now(timezone.utc))
    await session.execute(stmt)
    await session.commit()
    logger.info(f"set_last_check_time: tg_id={tg_id}, обновлено время последней проверки")


async def get_user_achievement_number(session: AsyncSession, tg_id: int) -> int:
    """Получаем номер достижения пользователя по tg_id."""
    stmt = select(User.achievement).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    achievement = result.scalar()
    logger.info(f"get_user_achievement_number: tg_id={tg_id}, номер достижения={achievement}")
    return achievement


async def increase_user_achievement_number(session: AsyncSession, tg_id: int) -> None:
    """Прибавляем достижения пользователя на 1 по tg_id."""
    stmt = select(User.achievement).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    achievement = result.scalar()

    update_stmt = update(User).where(User.tg_id == tg_id).values(achievement=achievement + 1)
    await session.execute(update_stmt)
    await session.commit()


async def reset_user_achievements(session: AsyncSession, tg_id: int) -> None:
    """Сброс достижений пользователя при повторной проверке."""
    stmt = select(User.last_check_date).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    last_check_date = result.scalar()

    if last_check_date:
        update_stmt = update(User).where(User.tg_id == tg_id).values(achievement=2)
    else:
        update_stmt = update(User).where(User.tg_id == tg_id).values(achievement=1)

    await session.execute(update_stmt)
    await session.commit()


async def set_user_action(session: AsyncSession, tg_id: int, action: str) -> None:
    """Фиксируем действия пользователя в логах."""
    action_description = ACTION_TEMPLATES[action]
    result = await session.execute(select(User))
    users = result.scalars().all()

    new_action = Log(
        user_id=tg_id,
        action=action_description,
        create_date_time=datetime.now(timezone.utc)
    )
    session.add(new_action)
    await session.commit()
    logger.info(f"set_user_action: tg_id={tg_id}, действие={action_description} сохранено")


async def save_payment(session: AsyncSession, tg_id: int, payment_id: str) -> None:
    """Сохраняем новый платеж в базе."""
    payment = Payment(user_id=tg_id, payment_id=payment_id, status="pending")
    session.add(payment)
    await session.commit()
    logger.info(f"save_payment: tg_id={tg_id}, новый платёж с payment_id={payment_id} сохранён")


async def get_unpaid_payments(session: AsyncSession) -> list[tuple[str, int]]:
    """Получаем список незавершённых платежей."""
    async with session.begin():
        result = await session.execute(
            select(Payment.payment_id, Payment.user_id).where(Payment.status == "pending")
        )
        return result.fetchall()


async def update_payment_status(session: AsyncSession, payment_id: str, status: str) -> None:
    """Проверяем и обновляем статус платежа по payment_id."""
    logger.info(f"update_payment_status: обновляем статус для payment_id={payment_id}")

    query = select(Payment).where(Payment.payment_id == payment_id)
    result = await session.execute(query)

    payment = result.scalar_one_or_none()

    if payment:
        logger.info(f"update_payment_status: платёж найден, текущий статус={payment.status}")

        if payment.status != status:
            payment.status = status
            payment.payment_date = datetime.now(timezone.utc).replace(microsecond=0)
            await session.commit()
            logger.info(f"update_payment_status: статус обновлён на {status} для payment_id={payment_id}")
        else:
            logger.info(f"update_payment_status: статус уже {status}, обновление не требуется")
    else:
        logger.warning(f"update_payment_status: платёж с payment_id={payment_id} не найден")


async def check_payment_status(session: AsyncSession, payment_id: str) -> str:
    """Проверяем и обновляем статус платежа по payment_id."""
    logger.info(f"update_payment_status: проверка статуса для payment_id={payment_id}")

    result = await session.execute(
        select(Payment.status).where(Payment.payment_id == payment_id)
    )
    payment_status = result.scalar()
    return payment_status


async def set_user_payment_date(session: AsyncSession, tg_id: int) -> None:
    """Проверяем текущую подписку и обновляем."""
    now = datetime.now(timezone.utc).replace(microsecond=0)

    stmt_select = select(User.payment_end_date).where(User.tg_id == tg_id)
    result = await session.execute(stmt_select)
    current = result.scalar_one() or now

    base_date = current if current > now else now
    new_date = datetime.combine(base_date.date(), now.time(), tzinfo=timezone.utc) + timedelta(days=30)

    stmt_update = (
        update(User)
        .where(User.tg_id == tg_id)
        .values(payment_end_date=new_date)
    )

    await session.execute(stmt_update)
    await session.commit()

async def get_user_payment_date(session: AsyncSession, tg_id: int) -> Optional[datetime]:
    """Запрашиваем дату окончания подписки."""
    stmt = select(User.payment_end_date).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    payment_end_date = result.scalar_one_or_none()
    return payment_end_date


async def get_step_progress(session: AsyncSession, tg_id: int, step_id: str) -> Optional[str]:
    """Получаем статус прохождения актуального шага."""
    stmt = select(SecurityStepProgress.status).where(
        SecurityStepProgress.user_id == tg_id,
        SecurityStepProgress.step_id == step_id
    )
    result = await session.execute(stmt)
    status = result.scalar_one_or_none()
    return status



async def create_step_progress(session: AsyncSession, tg_id: int, step_id: str, status: str = "started") -> None:
    """Создает запись о начале шага проверки безопасности."""
    new_step = SecurityStepProgress(
        user_id=tg_id,
        step_id=step_id,
        status=status
    )
    session.add(new_step)
    await session.commit()


async def update_step_progress(session: AsyncSession, tg_id: int, step_id: str, status: str = "completed") -> None:
    """Обновляет статус шага (например, 'completed')."""
    stmt = (
        update(SecurityStepProgress)
        .where(SecurityStepProgress.user_id == tg_id, SecurityStepProgress.step_id == step_id)
        .values(status=status)
    )
    await session.execute(stmt)
    await session.commit()


async def get_current_step(session: AsyncSession, tg_id: int):
    """Получить актуальный шаг проверки."""
    progress = await session.execute(
        select(SecurityStepProgress).filter_by(user_id=tg_id).order_by(SecurityStepProgress.timestamp.desc())
    )
    step = progress.scalar()
    return step.step_id if step else None


async def delete_user_steps(session: AsyncSession, tg_id: int):
    """Очищаем историю проверки пользователя."""
    await session.execute(
        delete(SecurityStepProgress).where(SecurityStepProgress.user_id == tg_id)
    )
    await session.commit()