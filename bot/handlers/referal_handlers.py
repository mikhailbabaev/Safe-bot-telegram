import asyncio
import random
import os
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from handlers.states import MyStates
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.common_keyboards import to_start_menu
from keyboards.referal_kb import referal_getout_kb, referal_kb
from templates import REFERAL, REFERAL_GET_OUT, PROMOCODE_GIVEN, LINK
from database.requests import get_promocode_by_tg_id, set_promocode_given, get_user_by_tg_id, set_promocode_usage, get_tg_id_by_promocode, set_promocode_is_active, check_promocode_is_active

ref_router = Router()


@ref_router.callback_query(F.data == "cashback")
async def cashback_menu(callback: types.CallbackQuery, session: AsyncSession):
    await callback.answer(show_alert=False)
    tg_id = callback.from_user.id
    promocode = await get_promocode_by_tg_id(session, tg_id)
    message = REFERAL.format(promocode=promocode)
    await callback.message.answer(
        message,
        reply_markup=referal_kb,
        parse_mode="HTML"
    )



@ref_router.callback_query(F.data == "use_promocode")
async def start_handlers(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(show_alert=False)
    await state.set_state(MyStates.waiting_for_input)
    await callback.message.answer("Введите промокод:")


@ref_router.message(MyStates.waiting_for_input)
async def process_input(message: types.Message, state: FSMContext, session: AsyncSession):
    promocode = message.text.strip()
    # взяли промокод
    user_tg_id = message.from_user.id
    id_user_from_db = await get_tg_id_by_promocode(session, promocode) # нашли tg_id пользователя через промокод
    if user_tg_id == id_user_from_db:
        # если tg_id совпадают, то ошибка
        await message.answer(("🚫 Вы не можете использовать собственный промокод."))
    else:
        # проверяем, может у пользователя уже активирован промокод
        check_promo = await check_promocode_is_active(session, user_tg_id)
        if check_promo:
            await message.answer(("У вас уже активирован промокод со скидкой!"))
        else:
            await set_promocode_usage(session, id_user_from_db)
            await set_promocode_is_active(session, user_tg_id, promocode)
            await message.answer(f"Промокод {promocode} успешно активирован!", reply_markup=to_start_menu)
    await state.clear()



@ref_router.callback_query(F.data == "withdraw_money")
async def withdraw_money(callback: types.CallbackQuery):
    await callback.answer(show_alert=False)
    await callback.message.answer(
        REFERAL_GET_OUT,
        reply_markup=referal_getout_kb,
        parse_mode="HTML"
    )



@ref_router.callback_query(F.data == "copy_promocode")
async def copy_promocode(callback: types.CallbackQuery, session: AsyncSession):
    await callback.answer(show_alert=False)
    tg_id = callback.from_user.id
    promocode = await get_promocode_by_tg_id(session, tg_id)
    message_text = PROMOCODE_GIVEN.format(link=LINK) + f" {promocode}"
    await set_promocode_given(session, tg_id)
    await callback.message.answer(
        message_text,
        parse_mode="HTML",
        reply_markup=to_start_menu
    )

