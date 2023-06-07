from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app import repo
from app.bot.handlers.callbackdata import StartCb, GoToCb, SettingsCb, SettingsLanguageCb
from app.bot.handlers.keyboards.settings import settings_menu_keyboard, settings_language_keyboard
from app.misc import locale_manager

settings_router = Router()


@settings_router.callback_query(StartCb.filter(F.action == 'settings'))
async def settings_menu_handler(call: CallbackQuery, state: FSMContext, _):
    await call.message.delete()
    await call.message.answer(text=_("messages.settings"), reply_markup=settings_menu_keyboard(_))


@settings_router.callback_query(GoToCb.filter(F.action == 'settings'))
async def go_to_settings_handler(call: CallbackQuery, state: FSMContext, _):
    await settings_menu_handler(call, state, _)


"""Language"""


@settings_router.callback_query(SettingsCb.filter(F.action == 'language'))
async def settings_language_menu_handler(call: CallbackQuery, state: FSMContext, _):
    await call.message.delete()
    await call.message.answer(text=_("messages.settings_language"), reply_markup=settings_language_keyboard(_))


@settings_router.callback_query(SettingsLanguageCb.filter())
async def settings_language_choose_handler(call: CallbackQuery, state: FSMContext, _):
    call_data = SettingsLanguageCb.unpack(call.data)
    user = await repo.users.get(call.message.chat.id)
    await repo.users.update(user, locale=call_data.action)
    _ = locale_manager.get_locale(call_data.action).get
    await settings_menu_handler(call, state, _)
