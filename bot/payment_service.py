import asyncio
from payments import check_payment_status  # Это твоя функция для проверки статуса платежа
from payment_service import get_unpaid_payments, update_payment_status
from aiogram import Bot

async def check_payment_status(payment_id: str):
    """Проверка статуса платежа в ЮKassa"""
    payment = Payment.find_one(payment_id)
    return payment.status


async def poll_payments(bot: Bot, session: AsyncSession):
    """Фоновая проверка платежей"""
    while True:
        # Получаем список незавершённых платежей
        unpaid_payments = await get_unpaid_payments(session)

        # Проходим по всем платежам и проверяем их статус
        for payment_id, tg_id in unpaid_payments:
            status = await check_payment_status(payment_id)

            # Если платёж успешен, обновляем статус
            if status == "succeeded":
                await update_payment_status(session, payment_id, "succeeded")

                # Отправляем сообщение пользователю о том, что оплата прошла
                await bot.send_message(tg_id, "✅ Оплата прошла успешно! Доступ открыт.")

        # Задержка перед следующей проверкой
        await asyncio.sleep(30)