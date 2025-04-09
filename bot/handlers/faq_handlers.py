from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.faq_kb import FAQ
from templates import FAQ_TEXT
from database.requests import set_user_action

faq_router = Router()


@faq_router.callback_query(F.data == "FAQ")
async def show_faq(callback: CallbackQuery, session: AsyncSession):
    """Показываем информацию о FAQ с кнопкой возврата в главное меню"""
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, "faq")

    await callback.message.answer(
        FAQ_TEXT,
        reply_markup=FAQ,
        parse_mode="HTML"
    )
    await callback.answer()