from aiogram import Router
from aiogram.filters import Command

from consbot.bot.dialogs.commands import start_command
from consbot.utils.bot.commands import Commands


def register_dialogs(root_router: Router) -> None:
    dialog_router = Router()
    dialog_router.include_routers(
        admin_dialog_router,
        consultant_dialog_router,
        regular_dialog_router,
    )
    dialog_router.message(Command(Commands.START))(start_command)
    root_router.include_router(dialog_router)
