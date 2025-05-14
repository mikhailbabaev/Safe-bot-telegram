import logging
from datetime import datetime, timezone

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
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
    get_wallet_count,
    reset_user)

router = Router()
logger = logging.getLogger(__name__)


def get_welcome_message(is_paid: bool, payment_date: datetime | None = None, wallet_count: float = 0) -> str:
    if is_paid and payment_date:
        return (
            f"{WELCOME_MESSAGE}\n"
            f"✅ Ваша подписка активна до: {payment_date.strftime('%d.%m.%Y %H:%M')}\n"
            f"На вашем личном счету {wallet_count} рублей"
        )
    else:
        return (
            f"{WELCOME_MESSAGE}\n"
            "⚠️ У вас нет активной подписки или срок действия истёк. "
            f"На вашем личном счету {wallet_count} рублей"

        )


async def show_main_menu(message: Message, chat_id: int, session: AsyncSession):
    now = datetime.now(timezone.utc)
    wallet_count = await get_wallet_count(session, chat_id)
    payment_date = await get_user_payment_date(session, chat_id)
    achievement_number = await get_user_achievement_number(session, chat_id)
    is_paid = payment_date is not None and payment_date > now
    achievement_text = ACHIEVEMENT_LIST.get(achievement_number, "🏆 Достижения")
    keyboard = get_start_menu(achievement_text, is_paid, wallet_count)
    welcome_text = get_welcome_message(is_paid, payment_date, wallet_count)
    await message.answer_photo(
        photo='AgACAgIAAxkBAAIIyGgN_YNdefF_beYa1bWFDDlv-DoEAAI76DEbLQtwSGHr_xSMi80TAQADAgADeQADNgQ',
        caption=welcome_text,
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

    await show_main_menu(message, tg_id, session)
    await set_user_action(session, tg_id, 'start')

    logger.warning(
        f"Аутентификация: ID={tg_id}, Username={username}, Имя={first_name}, Фамилия={last_name}, Время={datetime.now()}"
    )


@router.callback_query(F.data == "go_to_start_menu")
async def return_to_main_menu(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, 'go_to_start_menu')
    await state.clear()
    await show_main_menu(callback.message, tg_id, session)
    await callback.answer()


# Отладочные обработчики для получения id файлов

@router.message(F.text == "/reset")
async def reset_command_handler(message: Message, session: AsyncSession):
    tg_id = message.from_user.id
    await reset_user(session, tg_id)
    await message.answer("Сброс выполнен")


# Обработчики ниже используются для подгрузки медиа файлов в чат и получения их id в этом чате

# @router.message(F.photo)
# async def photo(message: Message):
#     file_id_photo = message.photo[-1].file_id
#     print(file_id_photo)
#     await message.answer(f"✅ Сохрани этот file_id: `{file_id_photo}`")


# @router.message(F.document)
# async def handle_video(message: Message):
#     file_id = message.document.file_id
#     print(file_id)
#     await message.answer_photo(file_id)
#     await message.answer(f"✅ Сохрани этот file_id: `{file_id}`")




