from aiogram import Router, F

from aiogram.types import CallbackQuery,  FSInputFile
from templates import PAYMENT_TEXT
from keyboards.payment_kb import create_payments_keyboard
from database.requests import set_user_action, save_payment
from sqlalchemy.ext.asyncio import AsyncSession

import uuid
import os
from yookassa import Payment, Configuration
from dotenv import load_dotenv

load_dotenv()


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

pay_router = Router()


@pay_router.callback_query(F.data == "payments")
async def payment_to_ukassa(callback: CallbackQuery, session: AsyncSession):
    """Оплата сервиса через Юкассу"""
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, 'pay')

    payment_id, payment_url = await create_payment(9.00, tg_id)
    await save_payment(session, tg_id, payment_id)

    image_path = os.path.join(os.path.dirname(__file__), '../pay.jpg')
    image_file = FSInputFile(image_path)

    payments = create_payments_keyboard(payment_url)

    await callback.message.answer_photo(
        image_file,
        caption=PAYMENT_TEXT,
        reply_markup=payments,
        parse_mode='HTML'
    )
    await callback.answer(show_alert=False)


