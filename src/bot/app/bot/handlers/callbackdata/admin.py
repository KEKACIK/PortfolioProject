from aiogram.filters.callback_data import CallbackData


class AdminCb(CallbackData, prefix="Admin"):
    action: str
