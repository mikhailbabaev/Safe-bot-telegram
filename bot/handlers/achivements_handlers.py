from aiogram import Router, F

from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.achivements_kb import achive_kb
from templates import ACHIVEMENTS
from database.requests import set_user_action


achivements_router = Router()


@achivements_router.callback_query(F.data == "achivements")
async def show_faq(callback: CallbackQuery, session: AsyncSession):
    """Показываем информацию о FAQ с кнопкой возврата в главное меню"""
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, "achievements")
    await callback.message.answer(
        ACHIVEMENTS,
        reply_markup=achive_kb,
        parse_mode="HTML"
    )
    await callback.answer()