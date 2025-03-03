from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from database.models import *

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False,
                 echo_pool: bool = False, pool_size: int = 5,
                 max_overflow: int = 10) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Асинхронный контекстный менеджер для сессии."""
        async with self.session_factory() as session:
            yield session
            await session.commit()

    async def init_db(self) -> None:
        """Метод для инициализации базы данных (например, создание таблиц)."""

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def dispose(self) -> None:
        """Ожидаем завершения работы с соединением."""
        await self.engine.dispose()

