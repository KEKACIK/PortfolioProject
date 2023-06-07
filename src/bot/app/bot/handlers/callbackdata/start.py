from aiogram.filters.callback_data import CallbackData


class GoToCb(CallbackData, prefix="GoTo"):
    action: str


class StartCb(CallbackData, prefix="Start"):
    action: str
