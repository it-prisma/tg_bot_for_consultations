from aiogram.filters import BaseFilter
from aiogram.types import Message

from consbot.config import Settings
from consbot.db.models import User, UserRole


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, settings: Settings) -> bool:
        if message.from_user and message.from_user.id in settings.ADMINS:
            return True
        return False


class ConsultantFilter(BaseFilter):
    async def __call__(self, message: Message, user: User) -> bool:
        if user.role == UserRole.CONSULTANT:
            return True
        return False
