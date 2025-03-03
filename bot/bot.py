import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from database import DatabaseHelper
from handlers.handlers import router


# URL подключения к базе данных
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:Evgeniy-1@localhost/skum_bot_db')


async def main():
    load_dotenv()
    db_helper = DatabaseHelper(DATABASE_URL, echo=False)
    await db_helper.init_db()

    # Создаем объект бота и диспетчера
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(router)

    await dp.start_polling(bot)
    await db_helper.dispose()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log', mode='a', encoding='utf-8'),
        ]
    )
    try:
        asyncio.run(main())  # Запускаем асинхронную функцию main
    except KeyboardInterrupt:
        print('Бот выключен!')
