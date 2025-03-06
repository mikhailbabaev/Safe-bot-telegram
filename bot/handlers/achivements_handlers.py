from aiogram import Router, F

from aiogram.types import CallbackQuery

from keyboards.achivements_kb import achive_kb
from templates import ACHIVEMENTS


achivements_router = Router()


@achivements_router.callback_query(F.data == "achivements")
async def show_faq(callback: CallbackQuery):
    """Показываем информацию о FAQ с кнопкой возврата в главное меню"""
    await callback.message.answer(
        ACHIVEMENTS,
        reply_markup=achive_kb,
        parse_mode="HTML"
    )
    await callback.answer()