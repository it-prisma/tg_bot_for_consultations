from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import User as TGUser

from consbot.config import Settings
from consbot.db.holder import DatabaseHolder


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any | None:
        holder: DatabaseHolder = data["holder"]
        settings: Settings = data["settings"]
        tg_user: TGUser = data["event_from_user"]
        user = await holder.user.get_or_create(
            tg_user.id, is_admin=(tg_user.id in settings.ADMINS)
        )
        if not user.is_active:
            await event.bot.send_message(  # type: ignore[union-attr]
                user.id, "К сожалению вы внесены в черный список"
            )
            return None
        data["user"] = user
        return await handler(event, data)
