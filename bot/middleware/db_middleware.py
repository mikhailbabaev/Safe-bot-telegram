from typing import Callable
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiohttp import web
from aiogram import types

from database.db_helper import DatabaseHelper

class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db_helper: DatabaseHelper):
        super().__init__()
        self.db_helper = db_helper

    async def __call__(self, handler, *args):
        if isinstance(args[0], types.Update):
            # Для aiogram: обработка событий Telegram
            event = args[0]
            data = args[1] if len(args) > 1 else {}
            async with self.db_helper.get_session() as session:
                data["session"] = session  # Сохраняем сессию для aiogram
                return await handler(event, data)

        elif isinstance(args[0], web.Request):
            # Для aiohttp: обработка HTTP-запроса
            request = args[0]
            async with self.db_helper.get_session() as session:
                request['db_session'] = session  # Сохраняем сессию в запросе
                return await handler(request)