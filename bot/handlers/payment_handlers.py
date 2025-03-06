from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from templates import FUNC_IN_DEV
from database.requests import set_payment_time, get_user_by_tg_id
from sqlalchemy.ext.asyncio import AsyncSession


pay_router = Router()


@pay_router.callback_query(F.data == "pay_to_ukassa")
async def pay_ukassa(callback: CallbackQuery, session: AsyncSession):
    """Показываем информацию о FAQ с кнопкой возврата в главное меню"""
    tg_id = callback.from_user.id
    await callback.message.answer(FUNC_IN_DEV)
    await set_payment_time(session, tg_id)
    await callback.answer()