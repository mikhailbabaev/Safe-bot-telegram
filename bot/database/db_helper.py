from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from .base import Base
from . import models


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Используем asynccontextmanager для корректной работы с async with."""
        async with self.session_factory() as session:
            yield session


async def init_db(db_helper):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_db_helper(url: str) -> DatabaseHelper:
    """Функция для создания и настройки DatabaseHelper."""
    return DatabaseHelper(
        url=url,
        echo=False,
        pool_size=5,
        max_overflow=10,
    )


