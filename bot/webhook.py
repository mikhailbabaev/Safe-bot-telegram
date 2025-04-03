from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession
from database.requests import update_payment_status


async def yookassa_webhook(request):
    """Обрабатываем уведомление от Юкассы о платеже"""
    data = await request.json()  # Получаем тело запроса в формате JSON
    event = data.get("event")
    print('пришел вебхук', data)

    if event == "payment.succeeded":
        payment_id = data["object"]["id"]  # Получаем ID платежа
        tg_id = data["object"]["metadata"]["user_id"]  # Получаем tg_id из metadata
        status = data["object"]["status"]
        print(payment_id, tg_id, status)

        # Достаем сессию из запроса
        session = request['db_session']
        await update_payment_status(session, payment_id, status)

    return web.Response(status=200)


# Создаём приложение aiohttp
webhook_app = web.Application()
webhook_app.router.add_post("/webhook", yookassa_webhook)
