from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_keyboard() -> InlineKeyboardMarkup:
    start_keyboard = InlineKeyboardBuilder()
    start_keyboard.row(
        InlineKeyboardButton(text="Консультанты", callback_data="consultants"),
        InlineKeyboardButton(text="Пользователи", callback_data="users"),
    )
    start_keyboard.row(InlineKeyboardButton(text="Жалобы", callback_data="complaints"))
    start_keyboard.row(InlineKeyboardButton(text="Статистика", callback_data="stat"))
    
    return start_keyboard.as_markup()
