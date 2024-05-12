import asyncio
from collections.abc import AsyncGenerator
from types import MappingProxyType

import orjson
from aiogram import Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from aiomisc_dependency import dependency
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from consbot.args import Parser
from consbot.bot.dialogs.router import register_dialogs
from consbot.bot.middlewares.base import IMiddleware
from consbot.bot.middlewares.storage import StorageMiddleware
from consbot.bot.middlewares.user import BanMiddleware, UserMiddleware
from consbot.utils.bot.handlers import on_unknown_intent, on_unknown_state
from consbot.utils.consultants.storage import ConsultantStorage
from consbot.utils.db import (
    create_async_engine,
    create_async_session_factory,
)
from consbot.utils.json import dumps
from consbot.utils.users.storage import UserStorage


def config_deps(parser: Parser) -> None:
    
    @dependency
    def bot() -> Bot:
        return Bot(
            token=parser.telegram.bot_token,
            parse_mode=parser.telegram.parse_mode,
        )

    @dependency
    def bot_storage() -> BaseStorage:
        if parser.debug:
            return MemoryStorage()
        return RedisStorage.from_url(
            url=str(parser.redis.redis_dsn),
            key_builder=DefaultKeyBuilder(with_destiny=True),
            json_loads=orjson.loads,
            json_dumps=dumps,
        )

    @dependency
    def user_middleware(
        user_storage: UserStorage,
    ) -> IMiddleware:
        return UserMiddleware(
            user_storage=user_storage,
            administrator_ids=parser.telegram.administrator_ids,
        )

    @dependency
    def ban_middleware(user_storage: UserStorage, bot: Bot) -> IMiddleware:
        return BanMiddleware(
            user_storage=user_storage,
            bot=bot,
        )

    @dependency
    def dispatcher(
        bot_storage: BaseStorage,
        user_middleware: IMiddleware,
        ban_middleware: IMiddleware,
    ) -> Dispatcher:
        dp = Dispatcher(
            storage=bot_storage,
            events_isolation=SimpleEventIsolation(),
        )
        dp.update.outer_middleware(user_middleware)  # type: ignore[arg-type]
        dp.update.outer_middleware(ban_middleware)  # type: ignore[arg-type]
        register_dialogs(dp)
        setup_dialogs(dp)
        dp.errors.register(
            on_unknown_intent,
            ExceptionTypeFilter(UnknownIntent),
        )
        dp.errors.register(
            on_unknown_state,
            ExceptionTypeFilter(UnknownState),
        )
        return dp

    @dependency
    async def engine() -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(
            connection_uri=str(parser.postgres.pg_dsn),
            echo=parser.debug,
        )
        yield engine
        await asyncio.shield(engine.dispose())

    @dependency
    async def session_factory(
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return create_async_session_factory(engine=engine)
    
    @dependency
    def user_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> UserStorage:
        return UserStorage(session_factory=session_factory)
    
    @dependency
    def consultant_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> ConsultantStorage:
        return ConsultantStorage(session_factory=session_factory)
    
    @dependency
    def storage_middleware(
        user_storage: UserStorage,
        consultant_storage: ConsultantStorage,
    ) -> IMiddleware:
        return StorageMiddleware(
            storages=MappingProxyType({
                "user_storage": user_storage,
                "consultant_storage": consultant_storage,
            }),
        )  
    
    return
