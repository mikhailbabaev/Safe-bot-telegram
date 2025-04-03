import asyncio
import random

import time
import os
import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession


from keyboards.common_keyboards import start_menu
from templates import WELCOME_MESSAGE, PAYMENT_TEXT
from database.requests import get_user_by_tg_id, create_user, get_user_achievement_text, set_user_action

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext):
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
    await set_user_action(session, tg_id, 'start')
    logger.warning(
        f"Аутентификация: ID={tg_id}, Username={username}, Имя={first_name}, Фамилия={last_name}, Время={datetime.now()}")


@router.callback_query(F.data == "go_to_start_menu")
async def return_to_main_menu(callback: CallbackQuery,  state: FSMContext, session: AsyncSession):
    """Возвращаем в главное меню с обновленным текстом"""
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, 'go_to_start_menu')

    await state.clear()
    await callback.message.answer(
        WELCOME_MESSAGE,
        reply_markup=start_menu
    )
    await callback.answer()