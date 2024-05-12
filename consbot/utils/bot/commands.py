from enum import StrEnum, unique

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


@unique
class Commands(StrEnum):
    START = "start"


async def set_ui_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command=Commands.START, description="Начать работу с ботом"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
    )
    return None
