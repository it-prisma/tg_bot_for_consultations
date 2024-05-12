import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent, Message
from aiogram_dialog import DialogManager

from consbot.utils.bot.dialogs import start_new_dialog

log = logging.getLogger(__name__)


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager) -> None:
    log.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "Бот был перезапущен для тех. обслуживания.\n"
            "Вы будете перенаправлены в главное меню."
        )
        message = event.update.callback_query.message
        if isinstance(message, Message):
            try:
                await message.delete()
            except TelegramBadRequest:
                pass
    await start_new_dialog(dialog_manager=dialog_manager)
    return None


async def on_unknown_state(event: ErrorEvent, dialog_manager: DialogManager) -> None:
    log.error("Restarting dialog: %s", event.exception)
    await start_new_dialog(dialog_manager=dialog_manager)
    return None
