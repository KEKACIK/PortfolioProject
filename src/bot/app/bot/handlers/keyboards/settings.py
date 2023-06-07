from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.handlers.callbackdata.settings import SettingsCb, SettingsLanguageCb
from app.bot.handlers.callbackdata.start import GoToCb


def settings_menu_keyboard(_) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text=_("buttons.settings_language"), callback_data=SettingsCb(action="language").pack()),
        InlineKeyboardButton(text=_("buttons.back"), callback_data=GoToCb(action="start").pack()),
        width=1
    )
    return keyboard.as_markup()


def settings_language_keyboard(_) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text=_("buttons.ru"), callback_data=SettingsLanguageCb(action="ru").pack()),
        InlineKeyboardButton(text=_("buttons.en"), callback_data=SettingsLanguageCb(action="en").pack()),
        InlineKeyboardButton(text=_("buttons.back"), callback_data=GoToCb(action="settings").pack()),
        width=1
    )
    return keyboard.as_markup()
