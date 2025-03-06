from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards import start_menu
from templates import WELCOME_MESSAGE


faq_router = Router()

@faq_router.callback_query(F.data == "go_to_start_menu")
async def return_to_main_menu(callback: CallbackQuery):
    """Возвращаем в главное меню с обновленным текстом"""

    await callback.message.answer(
        WELCOME_MESSAGE,
        reply_markup=start_menu
    )
    await callback.answer()