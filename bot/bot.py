import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiohttp import web

from handlers import router, faq_router, check_router, ref_router, achivements_router, pay_router
from middleware.db_middleware import DatabaseMiddleware
from database.db_helper import init_db, create_db_helper
from webhook import webhook_app


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    db_url = os.getenv("DB")
    db_helper = create_db_helper(db_url)

    await init_db(db_helper)
    dp.update.middleware(DatabaseMiddleware(db_helper))
    db_middleware = DatabaseMiddleware(db_helper)

    # Добавляем db_middleware в приложение
    webhook_app.middlewares.append(db_middleware)

    dp.include_routers(router, faq_router, check_router, ref_router, achivements_router, pay_router)

    runner = web.AppRunner(webhook_app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8080)
    await site.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log', mode='a', encoding='utf-8'),
        ]
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')

