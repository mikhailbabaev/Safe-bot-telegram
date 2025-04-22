import logging
from datetime import datetime, timezone

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.common_keyboards import get_start_menu
from templates import WELCOME_MESSAGE, ACHIEVEMENT_LIST
from database.requests import (
    get_user_by_tg_id,
    create_user,
    get_user_achievement_number,
    set_user_action,
    get_user_payment_date,
    )

router = Router()
logger = logging.getLogger(__name__)


def get_welcome_message(is_paid: bool, payment_date: datetime | None = None) -> str:
    if is_paid and payment_date:
        return (
            f"✅ Ваша подписка активна до: {payment_date.strftime('%d.%m.%Y %H:%M')}\n\n"
            f"{WELCOME_MESSAGE}"
        )
    else:
        return (
            "⚠️ У вас нет активной подписки или срок действия истёк.\n\n"
            f"{WELCOME_MESSAGE}"
        )


async def show_main_menu(bot: Bot, chat_id: int, session: AsyncSession):
    now = datetime.now(timezone.utc)

    payment_date = await get_user_payment_date(session, chat_id)
    achievement_number = await get_user_achievement_number(session, chat_id)
    is_paid = payment_date is not None and payment_date > now

    achievement_text = ACHIEVEMENT_LIST.get(achievement_number, "🏆 Достижения")
    keyboard = get_start_menu(achievement_text, is_paid)
    welcome_text = get_welcome_message(is_paid, payment_date)

    if is_paid:
        await bot.send_message(
            chat_id,
            text=welcome_text,
            reply_markup=keyboard
        )
    else:
        await bot.send_message(
            chat_id,
            text=welcome_text,
            reply_markup=keyboard
        )


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    tg_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    is_bot = message.from_user.is_bot

    user_auth = await get_user_by_tg_id(session, tg_id)
    if not user_auth:
        await create_user(session, tg_id, first_name, last_name, username, is_bot)

    await show_main_menu(message.bot, tg_id, session)
    await set_user_action(session, tg_id, 'start')

    logger.warning(
        f"Аутентификация: ID={tg_id}, Username={username}, Имя={first_name}, Фамилия={last_name}, Время={datetime.now()}"
    )


@router.callback_query(F.data == "go_to_start_menu")
async def return_to_main_menu(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, 'go_to_start_menu')
    await state.clear()
    await show_main_menu(callback.bot, tg_id, session)
    await callback.answer()