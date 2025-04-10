import asyncio
import os
import logging

from yookassa import Payment, Configuration

from database.requests import get_unpaid_payments, update_payment_status, set_payment_time

logger = logging.getLogger(__name__)


Configuration.account_id = os.getenv("YOOKASSA_SHOP_ID")
Configuration.secret_key = os.getenv("YOOKASSA_SECRET_KEY")


async def check_payment_status(payment_id: str) -> str:
    """Проверяем статус платежа через API Юкассы"""
    try:
        logging.info(f"Запрос статуса платежа для ID: {payment_id}")
        payment = Payment.find_one(payment_id)
        logging.info(f"Ответ от Юкассы для {payment_id}: {payment}")
        return payment.status
    except Exception as e:
        logging.error(f"Ошибка при проверке статуса платежа {payment_id}: {e}")
        return 'error'


async def poll_unpaid_payments(db_helper):
    """Периодически проверяем статус неоплаченных платежей"""
    while True:
        logging.info('Запущен поллинг неоплаченных платежей')

        async with db_helper.get_session() as session:
            unpaid_payments = await get_unpaid_payments(session)

            for payment in unpaid_payments:
                payment_id, tg_id = payment

                logging.info(f"Проверка платежа {payment_id}")
                status = await check_payment_status(payment_id)

                logging.info(f"Обновляем статус в БД: {payment_id} -> {status}")
                await update_payment_status(session, payment_id, status)
                await set_payment_time(session, tg_id)
        await asyncio.sleep(3600)
