import logging
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

from consbot.db.uow import UnitOfWork

log = logging.getLogger(__name__)


class UnitOfWorkMiddleware(BaseMiddleware):
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        async with self.uow:
            data["uow"] = self.uow
            result = await handler(event, data)
        return result
