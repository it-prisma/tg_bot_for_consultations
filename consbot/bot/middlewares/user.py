from collections.abc import Awaitable, Callable, Sequence
from typing import Any

from aiogram import Bot
from aiogram.types import Update
from aiogram.types import User as AiogramUser

from consbot.bot.middlewares.base import IMiddleware
from consbot.utils.users.models import User, UserTypes
from consbot.utils.users.storage import UserStorage


class UserMiddleware(IMiddleware):
    _administrator_ids: Sequence[int]
    _user_storage: UserStorage

    def __init__(
        self,
        user_storage: UserStorage,
        administrator_ids: Sequence[int],
    ):
        self._administrator_ids = administrator_ids
        self._user_storage = user_storage

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        aiogram_user: AiogramUser = data["event_from_user"]
        user = await self._get_or_create_user(aiogram_user=aiogram_user)
        data["user"] = user
        return await handler(event, data)

    async def _get_or_create_user(
        self,
        aiogram_user: AiogramUser,
    ) -> User:
        user = await self._user_storage.read_by_telegram_id(aiogram_user.id)
        if user is None:
            user_type = self._get_user_type(aiogram_user.id)
            user = await self._user_storage.create_user(
                telegram_id=aiogram_user.id,
                user_type=user_type,
                properties=dict(),
            )
        return user

    def _get_user_type(self, telegram_id: int) -> UserTypes:
        if telegram_id in self._administrator_ids:
            return UserTypes.ADMINISTRATOR
        return UserTypes.NOT_REGISTERED


class BanMiddleware(IMiddleware):
    _user_storage: UserStorage
    _bot: Bot

    def __init__(self, bot: Bot, user_storage: UserStorage) -> None:
        self._user_storage = user_storage
        self._bot = bot

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        user: User = data["user"]
        if not user.is_banned:
            return await handler(event, data)
        elif update_from := (event.message or event.callback_query):
            if update_from.from_user:
                await self._bot.send_message(
                    chat_id=update_from.from_user.id,
                    text="You are banned!",
                )
