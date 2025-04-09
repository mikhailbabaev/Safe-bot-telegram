from aiohttp import web

from database.requests import update_payment_status


async def yookassa_webhook(request):
    """Обрабатываем уведомление от Юкассы о платеже"""
    data = await request.json()
    event = data.get("event")
    print('пришел вебхук', data)

    if event == "payment.succeeded":
        payment_id = data["object"]["id"]
        tg_id = data["object"]["metadata"]["user_id"]
        status = data["object"]["status"]
        print(payment_id, tg_id, status)

        session = request['db_session']
        await update_payment_status(session, payment_id, status)

    return web.Response(status=200)

webhook_app = web.Application()
webhook_app.router.add_post("/", yookassa_webhook)
