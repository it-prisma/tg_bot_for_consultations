from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from loguru import logger

from src.db.holder import DatabaseHolder
from src.filters.role import AdminFilter
from src.routers.admin.keyboards import get_start_keyboard

router = Router()
router.message.filter(AdminFilter())

message = """
Консультанты
- одобрение заявок от новых консультантов
- блокировка консультантов
- общение с консультантами в личных чатах

Пользователи
- смена консультанта
- удаление заявок, нарушающих правила платформы
- общение с пользователем
- блокировка пользователей

Жалобы
- обработка жалоб от пользователей и консультантов

Статистика
- сводная информация о всех пользователях бота
"""

@router.message(Command("start"))
async def cmd_start(
    message: Message,
) -> None:
    await message.answer("Консультанты", reply_markup=get_start_keyboard())
    return


@router.callback_query(F.data == "stat")
async def consultants_menu(callback: CallbackQuery, holder: DatabaseHolder):
    message = []
    for c, u in zip(
        (holder.stat.consultants, holder.stat.admins, holder.stat.users),
        ("Консультанты", "Пользователи"),
    ):
        persons = await c()
        message.append(u)
        message.append(f"Всего: {persons['total']}")
        message.append(f"Активных: {persons['active']}")
        message.append(f"Неактивных: {persons['total']}")
        message.append("\n")

    # await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('\n'.join(message), reply_markup=get_start_keyboard())
