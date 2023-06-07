from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.handlers.callbackdata.start import StartCb


def start_menu_keyboard(_, is_admin: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text=_("buttons.start_settings"), callback_data=StartCb(action="settings").pack()),
        width=1
    )
    if is_admin:
        keyboard.row(
            InlineKeyboardButton(text=_("buttons.start_admin"), callback_data=StartCb(action="admin").pack()),
            width=1
        )
    return keyboard.as_markup()
