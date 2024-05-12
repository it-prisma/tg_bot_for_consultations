import logging

from aiogram import Bot, Dispatcher
from aiomisc import Service

from consbot.utils.bot.commands import set_ui_commands

log = logging.getLogger(__name__)


class AiogramBotService(Service):
    __dependencies__ = (
        "bot",
        "dp",
    )

    bot: Bot
    dp: Dispatcher

    async def start(self) -> None:
        log.info("Initialize bot")

        await set_ui_commands(self.bot)
        await self.bot.delete_webhook(drop_pending_updates=True)

        self.start_event.set()
        log.info("Start polling")
        await self.dp.start_polling(self.bot)
