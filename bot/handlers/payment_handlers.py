import os
import uuid
import asyncio
import logging
from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.types import CallbackQuery,  FSInputFile, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from yookassa import Payment, Configuration
from dotenv import load_dotenv

from templates import PAYMENT_TEXT
from keyboards.payment_kb import get_payment_url_kb, get_payment_menu_kb
from database.requests import set_user_action, save_payment, check_payment_status, check_promocode_is_active
from handlers.states import PaymentState
from handlers.common_handlers import show_main_menu
from handlers.checking_handlers import show_pay_check_menu


load_dotenv()
pay_router = Router()
logger = logging.getLogger(__name__)

Configuration.account_id = os.getenv("YOOKASSA_SHOP_ID")
Configuration.secret_key = os.getenv("YOOKASSA_SECRET_KEY")

payment_id = uuid.uuid4()


async def create_payment(amount: float, tg_id: int):
    """Создание платежа через ЮKassa"""
    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url":"https://t.me/test_antiugon_telegram_bot"
        },
        "capture": True,
        "description": f"Оплата подписки пользователем {tg_id}",
        "metadata": {
            "user_id": tg_id
        }
    })

    return payment.id, payment.confirmation.confirmation_url


async def wait_for_payment(message: Message,
                           session: AsyncSession,
                           state: FSMContext,
                           tg_id: int,
                           payment_id: str,
                           timeout: int = 300):

    start_time = datetime.now(timezone.utc).timestamp()

    while True:
        current_state = await state.get_state()
        if current_state != PaymentState.waiting_for_payment.state:
            logger.info(f"[FSM] Пользователь {tg_id} покинул состояние ожидания оплаты вручную.")
            return
        current_time = datetime.now(timezone.utc).timestamp()
        if current_time - start_time > timeout:
            await message.answer("⏳ Время на оплату истекло. Возвращаем вас в главное меню.")
            await state.clear()
            await show_main_menu(message, tg_id, session)
            logger.info(f"[FSM] Время истекло для user_id={tg_id}. Ожидание оплаты отменено.")
            return

        await asyncio.sleep(5)
        status = await check_payment_status(session, payment_id)

        if status == "succeeded":
            await message.answer("✅ Оплата подтверждена! Добро пожаловать!")
            await state.clear()
            await show_pay_check_menu(message, tg_id, session)
            return
        else:
            logger.info(f"[FSM] Ожидание подтверждения платежа для user_id={tg_id}...")


@pay_router.callback_query(F.data == "payments")
async def payment_to_ukassa(callback: CallbackQuery,
                            session: AsyncSession,
                            ):
    """Оплата сервиса через Юкассу"""
    tg_id = callback.from_user.id
    price = 149 if await check_promocode_is_active(session, tg_id) else 199
    await set_user_action(session, tg_id, 'pay')
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIIDGgN6ZUaszi8Wx664xiU7eaC_0dQAALa5jEbWT5xSF8ycevT81CSAQADAgADeQADNgQ",
        caption=PAYMENT_TEXT.format(price=price),
        reply_markup=get_payment_menu_kb(price),
        parse_mode='HTML'
    )

    await callback.answer(show_alert=False)


@pay_router.callback_query(F.data =="url_ukassa")
async def connection_ukassa(callback: CallbackQuery,
                            session: AsyncSession,
                            state: FSMContext):

    tg_id = callback.from_user.id
    price = 149 if await check_promocode_is_active(session, tg_id) else 199
    await set_user_action(session, tg_id, 'pay_to_ukassa')

    payment_id, payment_url = await create_payment(price, tg_id)
    await save_payment(session, tg_id, payment_id)

    await state.set_state(PaymentState.waiting_for_payment)
    await state.update_data(
        payment_id=payment_id,
        tg_id=tg_id,
        start_time=datetime.now(timezone.utc).timestamp()
    )
    await callback.message.answer(
        text="💳 Перейдите по ссылке для оплаты:",
        reply_markup=get_payment_url_kb(payment_url, price),
        parse_mode="HTML"
    )
    await callback.answer(show_alert=False)

    asyncio.create_task(wait_for_payment(callback.message, session, state, tg_id, payment_id))