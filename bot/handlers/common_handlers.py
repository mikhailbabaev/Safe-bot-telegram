import asyncio
import random
import os
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.common_keyboards import start_menu
from keyboards.payment_kb import payments
from templates import WELCOME_MESSAGE, PAYMENT_TEXT
from database.requests import get_user_by_tg_id, create_user, get_user_achievement_text

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    tg_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    is_bot = message.from_user.is_bot
    user_auth = await get_user_by_tg_id(session, tg_id)

    if user_auth:
        achievement_text = await get_user_achievement_text(session, tg_id)
        start_menu.inline_keyboard[3][0].text = achievement_text
        await message.answer(WELCOME_MESSAGE, reply_markup=start_menu)
    else:
        await create_user(session, tg_id, first_name, last_name, username, is_bot)
        achievement_text = await get_user_achievement_text(session, tg_id)
        start_menu.inline_keyboard[3][0].text = achievement_text
        await message.answer(WELCOME_MESSAGE, reply_markup=start_menu)


@router.callback_query(F.data == "payments")
async def payment_to_ukassa(callback: CallbackQuery):
    """Оплата сервиса через Юкассу"""
    image_path = os.path.join(os.path.dirname(__file__), '../pay.jpg')
    image_file = FSInputFile(image_path)
    await callback.message.answer_photo(
        image_file,
        caption=PAYMENT_TEXT,
        reply_markup=payments,
        parse_mode='HTML'
    )
    await callback.answer(show_alert=False)


@router.callback_query(F.data == "go_to_start_menu")
async def return_to_main_menu(callback: CallbackQuery,  state: FSMContext):
    """Возвращаем в главное меню с обновленным текстом"""
    await state.clear()
    await callback.message.answer(
        WELCOME_MESSAGE,
        reply_markup=start_menu
    )
    await callback.answer()