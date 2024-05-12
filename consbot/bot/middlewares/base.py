from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Update


class IMiddleware(ABC):
    @abstractmethod
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        raise NotImplementedError
