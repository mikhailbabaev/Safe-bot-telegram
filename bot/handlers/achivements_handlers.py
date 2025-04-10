from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.achivements_kb import achive_kb
from templates import ACHIVEMENTS, ACHIEVEMENT_LIST
from database.requests import set_user_action, get_user_achievement_number
from utils import get_user_achievement_text

achivements_router = Router()

@achivements_router.callback_query(F.data == "achivements")
async def show_faq(callback: CallbackQuery, session: AsyncSession):
    """Показываем информацию о достижениях пользователя с кнопкой возврата в главное меню"""
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, "achievements")

    # Получаем номер текущего достижения пользователя
    achievement_number = await get_user_achievement_number(session, tg_id)

    # Получаем текст достижений, разделяя на полученные и не полученные
    achievements_text = get_user_achievement_text(achievement_number, ACHIEVEMENT_LIST)

    # Формируем финальный текст для отправки
    message_text = f"Ваши достижения:\n\n{achievements_text}"

    # Отправляем сообщение с информацией о достижениях
    await callback.message.answer(
        message_text,
        reply_markup=achive_kb,
        parse_mode="HTML"
    )
    await callback.answer()
