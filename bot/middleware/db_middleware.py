from aiogram.types import TelegramObject
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from database.db_helper import DatabaseHelper

class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db_helper: DatabaseHelper):
        super().__init__()
        self.db_helper = db_helper

    async def __call__(self, handler, event: TelegramObject, data: dict):
        async with self.db_helper.get_session() as session:
            data["session"] = session
            return await handler(event, data)
