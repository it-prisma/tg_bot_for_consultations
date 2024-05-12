from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from aiogram.types import Update

from consbot.bot.middlewares.base import IMiddleware
from consbot.utils.db import AbstractStorage


class StorageMiddleware(IMiddleware):
    _storages: Mapping[str, AbstractStorage]

    def __init__(
        self,
        storages: Mapping[str, AbstractStorage],
    ) -> None:
        self._storages = storages

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        data.update(self._storages)
        return await handler(event, data)
