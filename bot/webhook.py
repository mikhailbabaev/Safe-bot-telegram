import logging
import os
from aiohttp import web

from database.requests import update_payment_status, set_user_payment_date

logger = logging.getLogger(__name__)


async def yookassa_webhook(request):
    """Обрабатываем уведомление от Юкассы о платеже"""
    try:
        data = await request.json()
        logger.info("Получены данные от Юкассы: %s", data)

        event = data.get("event")
        if event == "payment.succeeded":
            payment_id = data["object"]["id"]
            tg_id = int(data["object"]["metadata"]["user_id"])
            status = data["object"]["status"]

            logger.info(f"Платеж успешно выполнен. ID: {payment_id}, Статус: {status}, Пользователь: {tg_id}")

            session = request['db_session']
            await update_payment_status(session, payment_id, status)
            await set_user_payment_date(session, tg_id)
            print("Вебхук")
            logger.info(f"Статус платежа обновлен для payment_id={payment_id}")

        else:
            logger.warning(f"Необработанное событие: {event}")

        return web.Response(status=200)

    except Exception as e:
        logger.error(f"Ошибка при обработке уведомления от Юкассы: {e}")
        return web.Response(status=500)


webhook_app = web.Application()
webhook_app.router.add_post("/", yookassa_webhook)
