from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from consbot.bot.filters.role import ConsultantFilter

router = Router()
router.message.filter(ConsultantFilter())


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer("Привет консультант")
    return
