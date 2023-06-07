from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.handlers.callbackdata.admin import AdminCb
from app.bot.handlers.callbackdata.start import GoToCb


def admin_menu_keyboard(_) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text=_("buttons.admin_export_users"), callback_data=AdminCb(action="export_users").pack()),
        InlineKeyboardButton(text=_("buttons.admin_mailing"), callback_data=AdminCb(action="mailing").pack()),
        InlineKeyboardButton(text=_("buttons.back"), callback_data=GoToCb(action="start").pack()),
        width=1
    )
    return keyboard.as_markup()


"""Do mailing"""


def admin_mailing_select_language_keyboard(_) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text=_("buttons.ru"), callback_data=AdminCb(action="mailing_language_ru").pack()),
        InlineKeyboardButton(text=_("buttons.en"), callback_data=AdminCb(action="mailing_language_en").pack()),
        InlineKeyboardButton(text=_("buttons.back"), callback_data=GoToCb(action="admin").pack()),
        width=1
    )
    return keyboard.as_markup()


def admin_mailing_submit_keyboard(_) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text=_("buttons.admin_mailing_yes"), callback_data=AdminCb(action="mailing_yes").pack()),
        InlineKeyboardButton(text=_("buttons.back"), callback_data=GoToCb(action="admin").pack()),
        width=1
    )
    return keyboard.as_markup()
