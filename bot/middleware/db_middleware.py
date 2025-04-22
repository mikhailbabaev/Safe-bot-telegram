from typing import Callable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Update
from aiohttp import web
from database.db_helper import DatabaseHelper


class DatabaseMiddleware(BaseMiddleware):
    """Middleware для передачи сессии SQLAlchemy в хэндлеры aiogram"""

    def __init__(self, db_helper: DatabaseHelper):
        super().__init__()
        self.db_helper = db_helper

    async def __call__(self, handler: Callable[[Update, Dict[str, Any]], Any],
                       event: Update, data: Dict[str, Any]) -> Any:
        async with self.db_helper.get_session() as session:
            data["session"] = session
            try:
                return await handler(event, data)
            finally:
                await session.close()


def create_db_middleware(db_helper: DatabaseHelper):
    """Создаем middleware для Aiohttp с доступом к базе данных"""

    @web.middleware
    async def db_middleware(request, handler):
        async with db_helper.get_session() as session:
            request["db_session"] = session
            response = await handler(request)
        return response

    return db_middleware
