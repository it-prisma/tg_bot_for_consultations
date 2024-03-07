import asyncio
import logging

from aiogram import Bot, Dispatcher

from consbot.bot.dialogs.router import router
from consbot.bot.middlewares.settings import SettingsMiddleware
from consbot.bot.middlewares.uow import UnitOfWork, UnitOfWorkMiddleware
from consbot.bot.middlewares.user import UserMiddleware
from consbot.config import Settings
from consbot.db.engine import (
    build_db_connection_uri,
    create_engine,
    create_session_factory,
)

logging.basicConfig(level=logging.INFO)


async def main(settings: Settings) -> None:
    bot = Bot(token=settings.TOKEN.get_secret_value())
    dp = Dispatcher()

    engine = create_engine(
        connection_uri=build_db_connection_uri(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
        )
    )
    session_factory = create_session_factory(engine=engine)
    uow = UnitOfWork(session_factory=session_factory)
    dp.update.outer_middleware(SettingsMiddleware(settings=settings))
    dp.update.outer_middleware(UnitOfWorkMiddleware(uow=uow))
    dp.message.outer_middleware(UserMiddleware())
    # dp.callback_query.middleware()
    # router.message.outer_middleware(SettingsMiddleware(settings=settings))
    # router.message.outer_middleware(DatabaseMiddleware(session_factory=session_factory))
    # router.message.outer_middleware(UserMiddleware())

    dp.include_router(router=router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    settings = Settings()
    asyncio.run(main(settings))
