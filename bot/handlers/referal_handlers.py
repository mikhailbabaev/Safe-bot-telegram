from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from handlers.states import MyStates
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.common_keyboards import to_start_menu
from keyboards.referal_kb import referal_getout_kb, referal_kb
from keyboards.promocode_kb import promo_kb_wrong, promo_kb_activated, promo_kb_success
from templates import REFERAL, REFERAL_GET_OUT, PROMOCODE_GIVEN, LINK
from database.requests import (
    get_promocode_by_tg_id,
    set_promocode_given,
    set_promocode_usage,
    get_tg_id_by_promocode,
    set_promocode_is_active,
    check_promocode_is_active,
    set_user_action,
    get_wallet_count)


ref_router = Router()


@ref_router.callback_query(F.data == "cashback")
async def cashback_menu(callback: types.CallbackQuery, session: AsyncSession):
    await callback.answer(show_alert=False)
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, "promocodes")
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
    user_tg_id = message.from_user.id
    id_user_from_db = await get_tg_id_by_promocode(session, promocode)
    if user_tg_id == id_user_from_db:
        await message.answer("🚫 Вы не можете использовать собственный промокод.", reply_markup=promo_kb_wrong)
    else:
        check_promo = await check_promocode_is_active(session, user_tg_id)
        if check_promo:
            await message.answer("У вас уже активирован промокод со скидкой!", reply_markup=promo_kb_activated)
        else:
            check_exist_promo = await set_promocode_usage(session, id_user_from_db, promocode)
            if check_exist_promo:
                await set_promocode_is_active(session, user_tg_id, promocode)

                tg_id = user_tg_id
                await set_user_action(session, tg_id, "promo_code_used")

                await message.answer(f"Промокод {promocode} успешно активирован!",
                                     reply_markup=promo_kb_success)
            else:
                await message.answer("Такого промокода выдано не было. Проверьте корректность!",
                                     reply_markup=promo_kb_wrong)
    await state.clear()



@ref_router.callback_query(F.data == "withdraw_money")
async def withdraw_money(callback: types.CallbackQuery, session: AsyncSession, bot: Bot):
    tg_id = callback.from_user.id
    admin_tg_id = 1426355954

    await set_user_action(session, tg_id, "withdraw")

    wallet_count = await get_wallet_count(session, tg_id)
    if wallet_count == 0:
        await callback.answer(show_alert=False)
        await callback.message.answer(
            f"У вас нет средств для вывода. "
            f" Попросите знакомых приобрести нашу подписку по вашему промокоду и получите 50 рублей.",
            parse_mode="HTML"
        )
        return
    await callback.answer(show_alert=False)
    referal_get_out_message = REFERAL_GET_OUT.format(wallet_count=wallet_count)
    await callback.message.answer(
        referal_get_out_message,
        reply_markup=referal_getout_kb,
        parse_mode="HTML"
    )
    await bot.send_message(
        admin_tg_id,
        f"⚠️ Пользователь ID: {tg_id}"
        f"запросил вывод средств. У него на счету {wallet_count} рублей."
    )


@ref_router.callback_query(F.data == "copy_promocode")
async def copy_promocode(callback: types.CallbackQuery, session: AsyncSession):
    await callback.answer(show_alert=False)
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, "promo_code_issued")
    promocode = await get_promocode_by_tg_id(session, tg_id)
    message_text = PROMOCODE_GIVEN.format(link=LINK) + f" {promocode}"
    await set_promocode_given(session, tg_id)
    await callback.message.answer(
        message_text,
        parse_mode="HTML",
        reply_markup=to_start_menu
    )

