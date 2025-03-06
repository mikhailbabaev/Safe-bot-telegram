import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import router, faq_router, check_router, ref_router, achivements_router, pay_router
from middleware.db_middleware import DatabaseMiddleware
from database.db_helper import init_db, create_db_helper


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    db_url = os.getenv("DB")
    db_helper = create_db_helper(db_url)

    await init_db(db_helper)
    dp.update.middleware(DatabaseMiddleware(db_helper))

    dp.include_routers(router, faq_router, check_router, ref_router, achivements_router, pay_router)
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
