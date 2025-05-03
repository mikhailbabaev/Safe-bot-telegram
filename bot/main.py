import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiohttp import web

from handlers import router, faq_router, check_router, ref_router, achivements_router, pay_router
from middleware.db_middleware import DatabaseMiddleware, create_db_middleware
from database.db_helper import init_db, create_db_helper
from webhook import webhook_app
from polling import poll_unpaid_payments
from utils import on_shutdown


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='a', encoding='utf-8'),
    ]
)
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    db_url = os.getenv("DB")
    db_helper = create_db_helper(db_url)

    await init_db(db_helper)

    # middleware для aiogram
    dp.update.middleware(DatabaseMiddleware(db_helper))

    # middleware для aiohttp
    webhook_app.middlewares.append(create_db_middleware(db_helper))

    dp.include_routers(router, faq_router, check_router, ref_router, achivements_router, pay_router)


    runner = web.AppRunner(webhook_app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8080)
    await site.start()

    asyncio.create_task(poll_unpaid_payments(db_helper))

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')
