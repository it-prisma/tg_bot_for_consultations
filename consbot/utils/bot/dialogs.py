from aiogram_dialog import DialogManager, ShowMode, StartMode

from consbot.bot.dialogs.states import StartMenuSG
from consbot.utils.consultants.storage import ConsultantStorage
from consbot.utils.users.models import User


async def start_new_dialog(dialog_manager: DialogManager) -> None:
    user: User = dialog_manager.middleware_data["user"]
    consultant_storage: ConsultantStorage = dialog_manager.middleware_data[
        "consultant_storage"
    ]
    if user.is_anonymous:
        if await consultant_storage.has_pending_consultant_request(user.id):
            await dialog_manager.start(
                ConsultantPendingSG.wait,
                mode=StartMode.RESET_STACK,
                show_mode=ShowMode.SEND,
            )
        else:
            await dialog_manager.start(
                StartMenuSG.menu,
                mode=StartMode.RESET_STACK,
                show_mode=ShowMode.SEND,
            )
    elif user.is_admin:
        # TODO forward to admin menu
        pass
    elif user.is_consultant:
        # TODO forward to consultant menu
        pass
    elif user.is_regular:
        # TODO forward to regular menu
        pass
    else:
        raise ValueError("Unknown user type")
