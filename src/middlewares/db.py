from collections.abc import Awaitable, Callable, Coroutine
from typing import Any

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.holder import DatabaseHolder


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        async with self.session_factory() as session:
            data["session"] = session
            holder = DatabaseHolder(session=session)
            data["holder"] = holder
            logger.info("asdfasdfasfasdfasdf")
            print("asdfasdfasdf")
            result = await handler(event, data)
        return result
