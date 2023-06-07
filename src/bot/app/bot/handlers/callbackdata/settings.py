from aiogram.filters.callback_data import CallbackData


class SettingsCb(CallbackData, prefix="Settings"):
    action: str


class SettingsLanguageCb(CallbackData, prefix="SettingsLanguage"):
    action: str
