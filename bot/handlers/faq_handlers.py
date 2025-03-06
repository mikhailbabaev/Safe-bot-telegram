from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.faq_kb import FAQ
from templates import FAQ_TEXT


faq_router = Router()


@faq_router.callback_query(F.data == "FAQ")
async def show_faq(callback: CallbackQuery):
    """Показываем информацию о FAQ с кнопкой возврата в главное меню"""
    await callback.message.answer(
        FAQ_TEXT,
        reply_markup=FAQ,
        parse_mode="HTML"
    )
    await callback.answer()