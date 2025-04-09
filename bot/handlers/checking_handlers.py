import asyncio
import random

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.checking_kb import checking_menu
from templates import CHECKUP_TEXT, CHECKUP_END
from database.requests import set_last_check_time, set_user_action

check_router = Router()


async def send_typing_effect(message: Message, text_blocks: dict, delay: float = 1.0):
    """Функция для постепенной отправки текста, сохраняя форматирование и обновляя одно сообщение"""
    full_text = ""
    sent_message = await message.answer("Загрузка...", parse_mode="HTML")

    for key in sorted(text_blocks.keys()):
        full_text = "\n".join(list(text_blocks.values())[:key])
        await sent_message.edit_text(full_text.strip(), parse_mode="HTML")
        await asyncio.sleep(delay)


@check_router.callback_query(F.data == "check_security")
async def check_security(callback: CallbackQuery, session: AsyncSession):
    """Имитация проверки безопасности с красивым прогрессом"""
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, 'free_check')

    message = await callback.message.answer("Начинаем проверку безопасности...")
    total_steps = len(CHECKUP_TEXT)
    progress_message = await message.answer(progress_bar(0))

    for i in range(1, total_steps + 1):
        progress = (i / total_steps) * 100
        await progress_message.edit_text(progress_bar(int(progress)))

        await asyncio.sleep(random.uniform(1.0, 2.5))
        await message.edit_text(CHECKUP_TEXT[i])
    await progress_message.delete()
    await set_last_check_time(session,tg_id)
    await message.answer(CHECKUP_END, reply_markup=checking_menu)


def progress_bar(percent):
    filled = "█" * (percent // 10)
    empty = "░" * (10 - percent // 10)
    return f"[{filled}{empty}] {percent}%"
